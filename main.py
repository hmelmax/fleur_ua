import futurist
import logging

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from taskflow import engines
from taskflow.patterns import linear_flow as lf
from taskflow.patterns import unordered_flow as uf

from fleur_ua.tasks.search_category_task import SearchCategoryTask
from fleur_ua.tasks.one_category_task import OneCategoryTask


settings = get_project_settings()
configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


while True:
    search_category_flow = lf.Flow("search_category_flow")

    search_category_flow.add(SearchCategoryTask())

    with futurist.ProcessPoolExecutor(max_workers=1) as executor:

        e = engines.load(search_category_flow, executor=executor, engine='parallel')
        e.compile()
        e.run()

    from fleur_ua.db import DB

    db = DB()
    db.connect()
    categories = db.select_categories()
    db.disconnect()
    print(categories)

    main_flow = uf.Flow("main_flow")
    for item in categories:
        if categories.get(item).get("last_page") == categories.get(item).get("count"):
            categories.get(item)["last_page"] = str(0)
        one_category_flow = lf.Flow(item)
        for i in range(int(categories.get(item).get("last_page")), int(categories.get(item).get("count"))):
            print("append")
            one_category_flow.add(OneCategoryTask(item, i+1))
        main_flow.add(one_category_flow)

    with futurist.ProcessPoolExecutor(max_workers=32) as executor:
        e = engines.load(main_flow, executor=executor, engine='parallel')
        e.compile()
        e.run()