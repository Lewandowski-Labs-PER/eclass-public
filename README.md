# eclass-public - Anonymised E-CLASS data 2016-2019.

If you use this data please cite the physical review paper: [link]()

This data set can only be used for research purposes. Commercial use of this data is strictly not allowed.

Updated August 4th 2022
The data used in the above linked paper has been moved to the sub-directory PRPER data.
New versions of the anon_cis.csv, anon_pre.csv, and anon_post.csv files have been placed in the root directory. These new versions have fixed some issues with the old data, namely:
1. Students are now matched on their first/last names in addition to their college ID number. This adds around 2000 more matched students.
2. Removing courses from 2020 that were in the anon_cis file, which did not have any pre/post data associated with it. This reduces the stated total number of courses from 599 to 494.
3. Changes to the way duplicates are dropped from the data set to do this within a course, rather than across the whole data frame, which could remove students who have the same name, or take more than one course in the data set.
4. The anon_pre.csv data now contains scores on a 5-point scale, consistent with the PRPER paper and the anon_post.csv data. This was mistakenly reduced to a 3-point scale when originally added to the repo.
