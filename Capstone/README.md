## Project Context


-----

This project seeks to explore characteristics of Monarch Butterfly, Danaus plexippus, coloration both in and outside the visible spectrum. It primarily asks:

1) Does the current scientific understanding of Orange Coloration in Monarch Physiology match what is observed in this reflectance data?
2) What does reflectance in the Ultraviolet, and Infrared spectrum even look like?
3) If reflectance characteristics exhibit sexual dimorphism, can these traits be effectively modeled?
4) Should a model be developed, what does it imply about feature importance of wavelenghts outside the visible spectrum?

### Use Cases

The classifier could be applied to generate sex labels of specimens sampled with a similar hyperspectral imager where samples are no longer available. Any findings relating to non-visible features with high importance are valuable to the field of entomology and in expanding the human knowledge around butterfly coloration. 

### What is in this repo?

This repo contains the entire analysis including:

* Source data
* Cleaned and transformed data
* Jupyter Notebook covering data import and cleaning
* Jupyter Notebook covering statistical testing for question 1 above
* Jupyter Notebook covering some EDA and machine learning modeling of questions 2-4 above
* Writeup of the project and findings
* Basic application using Flask to access the classification model and make a prediction given some novel data

### Contributing and/or collaboration

This project was not developed with collaboration in mind specifically. If you have a curiosity to expand on this work, please reach out to me for permission to use the source or derived data for additional investigation. Any findings are free to share or discuss. Reach me at stuart.a.sims@gmail.com anytime!

## Overview

#### Reflectance

Reflectance is a frequently used optical property in remote sensing. If you want to explore the theory behind the response signal, [here is a good overview of reflectance in remote sensing](http://www.oceanopticsbook.info/view/overview_of_optical_oceanography/reflectances).  Common approaches typically use highly sensitive imaging sensors to collect data from satellites over large areas. In this application, a hpyerspectrometer (a camera that can measure reflectance at a number of different wavelengths of light) was used at close range in controlled conditions to isolate the signal of individual Monarch samples in a specific position.

#### Data Cleaning

The dataset certainly fits the large p, small n area with 96 complete rows and 994 features stored in columns. Two outlier detection methods were explored across the feature space including setting thresholds at 1.5*IQR* and a Z score based approach. I knew that I would be using a classifier that was robust to outliers at the time, so I ultimately did not do any replacement for identified outliers (such as 99th percentile replacement). Given such a small dataset, storing it as a csv and using pandas dataframes proved simple and effective approaches.

#### Visualization

The reflectance "curves" or more simply, line plots across the spectrum of reflectance, show an interesting story.

![Monarch Reflectance Curves]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/blog_reflectance_curves_all.JPG')

Visible coloration between 400 and 700nm exhibits comparatively low reflectance values compared to the UV (here, 342-397nm). Additionally, the mean values for male and female specimens are much closer in value throughout the visible spectrum than in infrared areas. Males tend to reflect more light in these areas up until ~ 1350nm where females reflect more light than males from ~1350-2500nm.


#### Statistical Testing

Three areas of light in the "Green", "Blue", and  "Red" portions of light were used to test for signficiant sexual dimorphism. Before approahcing testing in these areas, I tested for normality in a looped fashion using scipy.stats. Most of the features could be categorized as normal (977 did not fail the test for normality while 17 did).

![Scipy Stats Normal Test Results]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/normal_test.JPG')

Using independent samples t tests, at an alpha: 0.01, there was significant evidence to support:

* Blue wavelength (450.6nm to 510.1nm) reflectance differs between male and female Monarchs. (p = 0.00065)
* Green wavelength (531.2nm to 591nm) reflectance differs between male and female Monarchs. (p = 0.00061)
* Red wavelength (640.4nm to 690.6nm) reflectance differs between male and female Monarchs. (p = 5.56 * 10^-9)

These findings were in line with the working knowledge around Monarch Coloration and sexual dimorphism.

#### Modeling

Two primary questions emerged as I began modeling:

1) Can I reduce the feature space without sacrificing, or even to gain, performance?
2) What do feature importances tell us about areas of reflectance that differ greatly (and thus are more helpful to the model itself?

I started by using PCA to decompose the feature space into three features based on the elbow plot (though I used cumulative explained variance instead of individual contributing explanations, so my "elbow" is just raised in the air instead.

![PCA Elbow Plot]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/pca_variance_explained.JPG')

From there, I used plotly to visualize the labels across this three-dimensional, reduced feature space in an interactive way.
PCA worked quite well, with 94% of variance explained by these three components alone.

I also implemented T-SNE to see how PCA and T-SNE would differ. This was mostly for my own curiosity.

##### Classification

After implementing a random forest classifier with scikit-learn with cross validation, the best parameter combination emerged and provided 88% accuracy. However, this ended up overfitting to the training data and did not generalize as well as default parameters in the test set. Ultimately, the most performant model reached ~72% accuracy with an f1 score of 0.67 for Males and 0.76 for Females.



#### Feature importance

Inspecting the feature importances from the classifier (purity based) showed a number of features in the red areas of light which were unsurprising given the literature. However, it did include one feature in the near infrared region. Using permutation importance, wavelengths in the red spectrum also rose to the top along with the same NIR feature at 822.2NM. However, multicollinearity poses a risk in that it can be deceptive for interpreting feature importance when present. The model can essentially rely on the highly correlated features while one is permuted, resulting in a feature looking more, or less, important than it actually is.

To tackle multicollinearity, I generated an array of spearman correlation coefficients to inspect for multicollinearity and visualized it as a heatmap.

![Correlation Coefficient Heatmap]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/blog_spearman_r_heatmap.JPG'). Clearly, it was an issue to tackle given high correlation coefficients across hundreds of features.

Hierarchical clustering segmented the feature space into only 12 groups at a threshold of 20.
![Hierarchical Clustering of Feature Correlation Coefficients]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/hierarchical_clustering_features.JPG').

Retraining the model showed improvements to 75.9% accuracy and an F1 score of 0.72 for Males and 0.79 for females. 

Ultimately, features in the red wavelengths held the highest importance. NIR and SWIR regions held some predictive power as well though.


#### Visualization of Model

LIME helped in checking the decision making of the classifier. It allows checking a classifier's decision points and inspects the likelihood of the classification given the features and their relative contributions to the predicted label. I would highly recommend it for that "gut checking" step in interpreting model results from supervised learning.
![LIME: Locally Interpretable Model-Agnostic Explanations]('https://github.com/stuartasims/Springboard/blob/master/Capstone/references/notes/lime_results.JPG').


## Future Questions

1) Is there any biological importance to Monarch reflectance in the NIR And SWIR? Can they even sense those colors given their photoreception?
2) Could one of these wavelengths signal for infectious status? Might the common Protozoan Parasite OE have some unique response?
3) Will someone collect a lot more of this data for me so we can continue to build a body of knowledge around this?




