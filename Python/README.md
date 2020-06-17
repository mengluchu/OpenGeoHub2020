If you never used Python, please follow these steps:
1)	[Download and install Anaconda](https://docs.anaconda.com/anaconda/install/windows/)
2)	Create and activate conda environment
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
conda create --name env_name python=3.7
conda activate env_name  (replace env_name with your environment name)
3)	Install python packages
conda install GDAL 
#conda install -c http://pcraster.geo.uu.nl/pcraster/pcraster -c conda-forge #pcraster=4.3.0_rc1                  # For using PCRaster to calculate predictors 
conda install keras                   # for deep learning
Anaconda install Tensorflow  # for deep learning -  so far the easiest option for scaling tensorflow operations to gpu
             other packages:  numpy, pandas, matplotlib, spyder, Jupyter

      4) open spyder or jupyter notebook from conda environment: conda spyder

Using jupyter notebook
Run jupyter on conda environment (CE), three ways
1)	Conda install jupyter from CE
2)	Source activate CE 
3)	Conda install ipykernel (might be the best)
Then: python -m ipykernel install --user --name=firstEnv

