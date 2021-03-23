import pandas as pd
import numpy as np

class eclass_data:
    """
    A container class for the eclass data set that makes pulling chunks
    of the data easier

    """
    
    def __init__(self, route=''):
        self.pre = pd.read_csv(route + 'anon_pre.csv')
        self.post = pd.read_csv(route +'anon_post.csv')
        self.cis = pd.read_csv(route +'anon_cis.csv')
        self.first_year_id = self.cis[self.cis.Q18=='First year (introductory) lab'].ResponseId
        self.buffy_id = self.cis[self.cis.Q18=='Beyond the first year lab'].ResponseId
        
        
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
    
    def get_cis_intro(self):
        return self._get_data(pre_post_cis='cis', intro_buffy='intro')

    def get_cis_buffy(self):
        return self._get_data(pre_post_cis='cis', intro_buffy='bfy')

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'e': eclass_data()})