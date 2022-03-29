# Asterank-academic-dash-project
An academic project to learn how to use Dash Plotly
Hey there! It's my small project to get acquainted with Dash Plotly.
Dash is running on http://127.0.0.1:8050/

It is based on data from http://www.asterank.com/kepler.
## Asterank is a scientific and economic database of over 600,000 asteroids.
They've collected, computed, or inferred important data such as asteroid mass and composition from multiple scientific sources.
### Kepler Project API Overview
Asterank offers a basic queryable database for NASA's Kepler Project. It is a simple way to quickly apply constraints to a set of over 2,000 exoplanets and unconfirmed "objects of interest." The database supports comparators and specific criteria for all attributes provided by the Kepler Data Explorer. The database currently runs on mongodb and queries must adhere to mongo's json format for a 'find' operation. Information is refreshed nightly from the Kepler Data Explorer.
Response data formats:

* KOI - Object of Interest number
* A - Semi-major axis (AU)
* RPLANET - Planetary radius (Earth radii)
* RSTAR - Stellar radius (Sol radii)
* TSTAR - Effective temperature of host star as reported in KIC (k)
* KMAG - Kepler magnitude (kmag)
* TPLANET - Equilibrium temperature of planet, per Borucki et al. (k)
* T0 - Time of transit center (BJD-2454900)
* UT0 - Uncertainty in time of transit center (+-jd)
* PER - Period (days)
* UPER - Uncertainty in period (+-days)
* DEC - Declination (@J200)
* RA - Right ascension (@J200)
* MSTAR - Derived stellar mass (msol)

I added two categories to this list:
* star size: the size of the star the planet's orbiting  around depending on RSTAR in comparison with our Sun's size
* planet suitability: characteristics of the planet depending on gravity (RPLANET) and temperature (TPLANET) that shows the suitability of the planet for life.
