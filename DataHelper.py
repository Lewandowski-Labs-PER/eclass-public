import pandas as pd

class eclass_data:
    """
    A container class for the eclass data set that makes pulling chunks
    of the data easier

    """
    
    def __init__(self):
        self.pre = pd.read_csv('anon_pre.csv')
        self.post = pd.read_csv('anon_post.csv')
        self.cis = pd.read_csv('anon_cis.csv')
        self.first_year_id = self.cis[self.cis.Q18=='First year (introductory) lab'].ResponseId
        self.buffy_id = self.cis[self.cis.Q18=='Beyond the first year lab'].ResponseId
        
    def get_intro_pre(self):
        """
        Returns pre-survey results for intro students
            
        >>> e.get_intro_pre().shape
        (33876, 66)
        """
        return self.pre[self.pre.ResponseId.isin(self.first_year_id)]
    
    def get_intro_post(self):
        """
        Returns post-survey results for intro students
        
        >>> e.get_intro_post().shape
        (27087, 111)
        """
        return self.post[self.post.ResponseId.isin(self.first_year_id)]
    
    def get_intro_matched(self):
        pre = self.pre[self.pre.ResponseId.isin(self.first_year_id)]
        post = self.post[self.post.ResponseId.isin(self.first_year_id)]
        return pre.merge(post, on=['anon_student_id', 'ResponseId'], suffixes=['_pre', '_post'])
    
    def get_buffy_pre(self):
        """
        Returns pre-survey results for buffy students
        
        >>> e.get_buffy_pre().shape
        (5629, 66)
        """
        return self.pre[self.pre.ResponseId.isin(self.buffy_id)]
    
    def get_buffy_post(self):
        """
        Returns post-survey results for buffy students
        
        >>> e.get_buffy_post().shape
        (4006, 111)
        """
        return self.post[self.post.ResponseId.isin(self.buffy_id)]
    
    def get_buffy_matched(self):
        pre = self.pre[self.pre.ResponseId.isin(self.buffy_id)]
        post = self.post[self.post.ResponseId.isin(self.buffy_id)]
        return pre.merge(post, on=['anon_student_id', 'ResponseId'], suffixes=['_pre', '_post'])
    
    def get_cis_intro(self):
        return self.cis[self.cis.ResponseId.isin(self.first_year_id)]
    
    def get_cis_buffy(self):
        return self.cis[self.cis.ResponseId.isin(self.buffy_id)]


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'e': eclass_data()})