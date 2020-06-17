# Etude: deep learning in air pollution

Exploration of air pollution mapping and others. The very initial motivation is to learn the road-no2 relationships automatically than using buffers

* data_arrange.py: gather data, the original data are pcrastermaps of roads in 25 m buffer at coordinates of ground stations
* cnnap.py: explore a  simple deep cnn structure with augumentation, different batchsize, structure, activation, pooling strategies.
* airbase_oaq.csv: ground stations for global air pollution mapping, currently not including Australia. 
* Figures form result folder shows the MAE obtained using different settings.
* The predictors folder consists of 32x32xn np arrays for each road type. They are cropped from a larger array (arround 70*50)
#### current findings in setting 


* I obtained higer accuracy with dropout and batchnorm. The lowest mae is around 10. 
* Averagepooling is not as steady as maxpooling. Intuitively, averagepooling makes more sense because we always aggregate road length withn a buffer.
* Batch size setting to 100 obtained better results than 32 and 50. Does it make a difference between regression and classification problem?
* The modeling seems to converge at around 5 epochs, then overfitting starts
* The activation of the last layer is set to relu to indicate no negetive predictions and for better backprop, seems to perform better.
* With imageGenerator it seems to obtain a more steady result.

#### notes
Currently only using 2000 stations for trainging and 600 for testing
data augumentation assumes the inputs are images, with 1, 3, or 4 channels: grayscale, rgb, 
 
