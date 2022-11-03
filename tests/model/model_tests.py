import json
import pandas as pd
import sys
sys.path.append('/Users/philippjohn/Developer/strava-analytics/model')
from ActivityList import ActivityList


def main():
    with open('data/activities_public.json') as f:
        json_data = json.load(f)
    new_list = ActivityList(json_data)
    assert (isinstance(new_list.get_df(), pd.DataFrame) == True)
    assert (new_list.get_num_activities() == 35)
    assert (new_list.get_num_runs() > 0)
    assert (new_list.get_num_rides() > 0)
    assert (new_list.get_num_hikes() > 0)
    assert (new_list.get_num_walks() > 0)


if __name__ == "__main__":
    main()
