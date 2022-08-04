import pandas as pd
import numpy as np

class eclass_data:
    """
    A container class for the eclass data set that makes pulling chunks
    of the data easier
    
    All functions return pandas dataframes and can thus be interacted with
    exactly as with a pandas dataframe.
    
    Class attributes include the raw data sets for pre, post, and cis data.
    Class attributes also include the unique IDs for intro and BFY students
    as well as question IDs for the survey itself to extract out only survey
    data.
    
    TODO : make unit test for unique_students 
    """
    
    def __init__(self, route=''):
        self.pre = pd.read_csv(route + 'anon_pre.csv')
        self.post = pd.read_csv(route +'anon_post.csv')
        self.cis = pd.read_csv(route +'anon_cis.csv')
        self.cis['StartDate'] = pd.to_datetime(self.cis['StartDate'])
        self.first_year_id = self.cis[self.cis.Q18=='First year (introductory) lab'].ResponseId
        self.buffy_id = self.cis[self.cis.Q18=='Beyond the first year lab'].ResponseId
        self.pre_survey_question_ids = ['q01a', 'q01b',
       'q02a', 'q02b', 'q03a', 'q03b', 'q04a', 'q04b', 'q05a', 'q05b',
       'q06a', 'q06b', 'q07a', 'q07b', 'q09a', 'q09b', 'q10a', 'q10b',
       'q11a', 'q11b', 'q12a', 'q12b', 'q13a', 'q13b', 'q14a', 'q14b',
       'q15a', 'q15b', 'q16a', 'q16b', 'q17a', 'q17b', 'q18a', 'q18b',
       'q19a', 'q19b', 'q20a', 'q20b', 'q21a', 'q21b', 'q22a', 'q22b',
       'q23a', 'q23b', 'q24a', 'q24b', 'q25a', 'q25b', 'q26a', 'q26b',
       'q27a', 'q27b', 'q28a', 'q28b', 'q29a', 'q29b', 'q30a', 'q30b',
       'q31a', 'q31b',] # questions 40a and 40b are removed from this list since they are the discard questions
        self.post_survey_question_ids = ['q01a', 'q01b', 'q01c', 'q02a',
       'q02b', 'q02c', 'q03a', 'q03b', 'q03c', 'q04a', 'q04b', 'q04c',
       'q05a', 'q05b', 'q05c', 'q06a', 'q06b', 'q06c', 'q07a', 'q07b',
       'q07c', 'q09a', 'q09b', 'q09c', 'q10a', 'q10b', 'q10c', 'q11a',
       'q11b', 'q11c', 'q12a', 'q12b', 'q12c', 'q13a', 'q13b', 'q13c',
       'q14a', 'q14b', 'q14c', 'q15a', 'q15b', 'q15c', 'q16a', 'q16b',
       'q16c', 'q17a', 'q17b', 'q17c', 'q18a', 'q18b', 'q18c', 'q19a',
       'q19b', 'q19c', 'q20a', 'q20b', 'q20c', 'q21a', 'q21b', 'q21c',
       'q22a', 'q22b', 'q22c', 'q23a', 'q23b', 'q24a', 'q24b', 'q25a',
       'q25b', 'q26a', 'q26b', 'q27a', 'q27b', 'q28a', 'q28b', 'q28c',
       'q29a', 'q29b', 'q30a', 'q30b', 'q30c', 'q31a', 'q31b', ]  # questions 40a and 40b are removed from this list since they are the discard questions
        
        
    def _get_data(self, pre_post_cis=None, intro_buffy=None, unique_students=False):
        """
        returns survey data filtered by input filters
        
        parent function to be used below by get_XXX_XXX functions
        """
        pre_post_cis_filter = {'pre':self.pre, 'post':self.post, 'cis':self.cis}
        df = pre_post_cis_filter[pre_post_cis]
        
        student_levels = {'intro':self.first_year_id, 'bfy':self.buffy_id}
        student_level_filter = student_levels[intro_buffy]
        
        if unique_students == False:
            return df[df.ResponseId.isin(student_level_filter)]
        
        else:
            return df[df.ResponseId.isin(student_level_filter)].groupby('anon_student_id').head(1)
    
    def get_intro_pre(self, unique_students=False):
        """
        Returns pre-survey results for intro students
        
        If unique_students is set to True then it will return the first response
        of a student based on the anon_student_id
            
        >>> e.get_intro_pre().shape
        (33876, 66)
        
        >>> e.get_intro_pre(unique_students=True).shape
        (30067, 66)
        """
        return self._get_data(pre_post_cis='pre', intro_buffy='intro', unique_students=unique_students)

    def get_intro_post(self, unique_students=False):
        """
        Returns post-survey results for intro students
        
        If unique_students is set to True then it will return the first response
        of a student based on the anon_student_id
        
        >>> e.get_intro_post().shape
        (27087, 111)
        """
        return self._get_data(pre_post_cis='post', intro_buffy='intro', unique_students=unique_students)

    def get_intro_matched(self, unique_students=False):
        """
        Returns matched survey data for the pre and post data sets based on the student
        anon_student_id and the survey ResponseId.
        
        If unique_students is set to True then it will return the first response
        of a student based on the anon_student_id
        
        TODO: make unit test
        """
        pre = self.get_intro_pre(unique_students=unique_students)
        post = self.get_intro_post(unique_students=unique_students)
        return pre.merge(post, on=['anon_student_id', 'ResponseId'], suffixes=['_pre', '_post'])

    def get_buffy_pre(self, unique_students=False):
        """
        Returns pre-survey results for buffy students
        
        >>> e.get_buffy_pre().shape
        (5629, 66)
        """
        return self._get_data(pre_post_cis='pre', intro_buffy='bfy', unique_students=unique_students)

    def get_buffy_post(self, unique_students=False):
        """
        Returns post-survey results for buffy students
        
        >>> e.get_buffy_post().shape
        (4006, 111)
        """
        return self._get_data(pre_post_cis='post', intro_buffy='bfy', unique_students=unique_students)

    def get_buffy_matched(self, unique_students=False):
        """
        Returns matched survey data for the pre and post data sets based on the student
        anon_student_id and the survey ResponseId.
        
        If unique_students is set to True then it will return the first response
        of a student based on the anon_student_id
        
        TODO: make unit test
        """
        pre = self.get_buffy_pre(unique_students=unique_students)
        post = self.get_buffy_post(unique_students=unique_students)
        return pre.merge(post, on=['anon_student_id', 'ResponseId'], suffixes=['_pre', '_post'])
    
    def get_pre(self, unique_students=False):
        """
        Returns pre-survey data for all students regardless of intro or bfy status
        
        TODO : make unit test
        """
        intro = self.get_intro_pre(unique_students=unique_students)
        bfy = self.get_buffy_pre(unique_students=unique_students)
        return pd.concat([intro, bfy])
    
    def get_post(self, unique_students=False):
        """
        Returns post survey data for all students regardless of intro or bfy status
        
        TODO : make unit test
        """
        intro = self.get_intro_post(unique_students=unique_students)
        bfy = self.get_buffy_post(unique_students=unique_students)
        return pd.concat([intro, bfy])
    
    def get_matched(self, unique_students=False):
        """
        Returns survey data for all matched students regardless of intro or bfy status
        
        TODO : make unit test
        """
        intro = self.get_intro_matched(unique_students=unique_students)
        bfy = self.get_buffy_matched(unique_students=unique_students)
        return pd.concat([intro, bfy])
    
    def get_cis_intro(self):
        """
        Returns the CIS data for intro students
        
        TODO : make unit tests
        """
        return self._get_data(pre_post_cis='cis', intro_buffy='intro')

    def get_cis_buffy(self):
        """
        Returns the CIS data for bfy students
        
        TODO : make unit tests
        """
        return self._get_data(pre_post_cis='cis', intro_buffy='bfy')

    def get_cis(self):
        """
        Returns full CIS table
        """
        intro = self.get_cis_intro()
        bfy = self.get_cis_buffy()
        return pd.concat([intro, bfy])
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'e': eclass_data()})