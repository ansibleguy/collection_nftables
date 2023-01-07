from cProfile import Profile
from pstats import Stats
from io import StringIO
from datetime import datetime
from pathlib import Path

from ansible_collections.ansibleguy.nftables.plugins.module_utils.defaults import \
    CONFIG


def profiler(
        check, log_file: str = None, kwargs: dict = None,
        sort: str = 'tottime', show_top_n: int = 20
) -> (list, dict, bool, None):
    # note: https://stackoverflow.com/questions/10326936/sort-cprofile-output-by-percall-when-profiling-a-python-script
    # sort options: ncalls, tottime, cumtime
    _ = Profile()
    _.enable()

    if kwargs is None:
        kwargs = {}

    check(**kwargs)
    _.disable()
    result = StringIO()
    Stats(_, stream=result).sort_stats(sort).print_stats(show_top_n)
    cleaned_result = result.getvalue().splitlines()[:-1]
    del cleaned_result[1:5]
    cleaned_result = '\n'.join(cleaned_result)

    if log_file is not None:
        log_path = Path(CONFIG['path_log'])
        if not log_path.exists():
            log_path.mkdir()

        with open(f'{log_path}/{log_file}', 'a+', encoding='utf-8') as log:
            log.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')} | {cleaned_result}\n")

    else:
        print(cleaned_result)
