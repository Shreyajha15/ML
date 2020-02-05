use "C:\Users\kxr190005\Downloads\guns.dta"


/*setting as panel data*/
xtset stateid year
/*balanced panel data*/

gen lvio= ln(vio)
/* the histogram is skewed towards the left*/
histogram vio 
/* after taking log (vio), it becomes normally distributed*/
hist lvio

/*pooled OLS without cluster robust standard errors*/
reg lvio  mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall

/*pooled OLS with cluster robust standard errors*/
reg lvio  mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall, vce(cluster stateid)

/*Checking for heteroskedasticity*/
reg lvio  mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall

predict ehat, resid

graph twoway scatter ehat pop, yline(0)

/*entity fixed effect model*/
xtreg lvio mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall, fe vce(cluster stateid)

/* time and entity fixed effects */
xtreg lvio mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall i.year, fe vce(cluster stateid) 
/*Testing for the effect of time*/
. testparm i.year

* HUASMAN TEST
* HAUSMAN TEST DOES NOT WORK WITH ROBUST ERRORS, SO USE "STANDARD" ERRORS.
xtreg lvio  mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall,fe
estimates store fixed

* xtreg lwage educ exper exper2 tenure tenure2 black south union, re
xtreg lvio  mur rob incarc_rate pop avginc density pb1064 pw1064 pm1029 i.shall,re
estimates store random
hausman fixed random

* chi2<0  , this is significant at alpha=1%
* We reject the null hypothesis of "no endogenity"
* Therefore, we have endogenity
* We will proceed with Fixed Effects model as it is immune to endogenity
