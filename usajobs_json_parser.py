import json
import numpy as np
import pandas as pd

# This function takes in a JSON file, parses out the needed information, and
# appends it to a list
def parse(data):
    jobs = []
    for job in data['SearchResult']['SearchResultItems']:
        this_job = []
        job_obj = job['MatchedObjectDescriptor']
        # Some listings have an empty string instead of a Dept Name, if so we
        # want to replace the empty string with 'None'
        if len(job_obj['DepartmentName']) < 1:
            deptName = 'None'
        else:
            deptName = job_obj['DepartmentName']

        jobCat = job_obj['JobCategory'][0]['Name']
        jobCatSpecific = job_obj['JobCategory'][1]['Name']
        agency = job_obj['OrganizationName']
        positionID = job_obj['PositionID']
        locations = job_obj['PositionLocation']

        # Some listings have multiple locations. Since we can't use all of these
        # locations in our model, we will instead set these values equal to
        # 'MultipleLocations'. When building a model that includes location as a
        # feature we will drop rows with 'MultipleLocations'.
        if len(locations) > 1:
            city = 'MultipleLocations'
            country = 'MultipleLocations'
            state = 'MultipleLocations'
            latitude = np.NaN
            longitude = np.NaN
        else:
            city = locations[0]['CityName']
            city = city.split(',')[0]
            country = locations[0]['CountryCode']
            state = locations[0]['CountrySubDivisionCode']
            latitude = locations[0]['Latitude']
            longitude = locations[0]['Longitude']

        grade = job_obj['JobGrade'][0]['Code']
        lowGrade = job_obj['UserArea']['Details']['LowGrade']
        highGrade = job_obj['UserArea']['Details']['HighGrade']
        positionSalaryMax = job_obj['PositionRemuneration'][0]['MaximumRange']
        positionSalaryMin = job_obj['PositionRemuneration'][0]['MinimumRange']
        positionSalaryInterval = job_obj['PositionRemuneration'][0]['RateIntervalCode']
        positionSchedule = job_obj['PositionSchedule'][0]['Name']
        startDate = job_obj['PositionStartDate']
        positionTitle = job_obj['PositionTitle']
        positionURI = job_obj['PositionURI']
        publicationStartDate = job_obj['PublicationStartDate']
        qualificationSummary = job_obj['QualificationSummary']
        matchedObjectID = job['MatchedObjectId']
        relevanceRank = job['RelevanceRank']

        # Append each variable to this jobs temporary list
        this_job.append(deptName)
        this_job.append(jobCat)
        this_job.append(jobCatSpecific)
        this_job.append(agency)
        this_job.append(positionID)
        this_job.append(city)
        this_job.append(country)
        this_job.append(state)
        this_job.append(latitude)
        this_job.append(longitude)
        this_job.append(grade + '-' + lowGrade)
        this_job.append(grade + '-' + highGrade)
        this_job.append(positionSalaryMax)
        this_job.append(positionSalaryMin)
        this_job.append(positionSalaryInterval)
        this_job.append(positionSchedule)
        this_job.append(startDate)
        this_job.append(positionTitle)
        this_job.append(positionURI)
        this_job.append(publicationStartDate)
        this_job.append(qualificationSummary)
        this_job.append(matchedObjectID)
        this_job.append(relevanceRank)
        # Append this jobs information to the master list
        jobs.append(this_job)
    return jobs

# Define the column names for the DataFrames
cols = ['department','job_category','job_cat_specific','organization_name',
        'position_id','city','country','state','latitude','longitude',
        'low_grade','high_grade','max_salary','min_salary','salary_interval',
        'position_schedule','start_date','positon_title','position_uri',
        'posting_date','qualification_summary','matched_objID','relevance_rank']

# Parse the first JSON file and create a DataFrame
with open('usajobs_data1.json') as data_file:
    data = json.loads(data_file.read())
jobs_list = parse(data)
jobs_df1 = pd.DataFrame(jobs_list, columns=cols)
# Parse the seconds JSON file and create a DataFrame
with open('usajobs_data2.json') as data_file:
    data = json.loads(data_file.read())
jobs_list = parse(data)
jobs_df2 = pd.DataFrame(jobs_list, columns=cols)
# Concatenate the two DataFrames
dfs = [jobs_df1,jobs_df2]
df_combined = []
df_combined = pd.concat(dfs,ignore_index=True)
# Export combined DataFrame to csv file
df_combined.to_csv('usajobs.csv')
