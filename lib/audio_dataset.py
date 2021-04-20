import torch
from torch.utils.data import Dataset, DataLoader
import os
from lib.machinelearning import *
import numpy as np
import random
import math

class AudioDataset(Dataset):
        

    def __init__(self, basedir, paths, settings):
        self.paths = paths
        self.settings = settings
        self.samples = []
        self.augmented_samples = []
        self.length = 0
        self.training = False
		
        rebuild_cache = False
        for index,path in enumerate(paths):
            totalpath = os.path.join(basedir,path)
            print( "Loading in " + path )
            listed_files = os.listdir(totalpath)
            listed_files_size = len( listed_files )
            for file_index, file in enumerate(listed_files):            
                if( file.endswith(".wav") ):
                    print( str( math.floor(((file_index + 1 ) / listed_files_size ) * 100)) + "%", end="\r" )
                    full_filename = os.path.join(totalpath, file)
                    
                    # When the input length changes due to a different input type being used, we need to rebuild the cache from scratch
                    if (index == 0 and file_index == 0):
                        rebuild_cache = len(self.feature_engineering_cached(full_filename, False)) != len(self.feature_engineering_augmented(full_filename))
                        print( "SHOULD REBUILD? " + str(rebuild_cache) )
                        
                    self.samples.append([full_filename, index, torch.tensor(self.feature_engineering_cached(full_filename, rebuild_cache)).float()])

    def append_augmentation_ids(self, training_ids, augmentation_probability=1.0):
        print( "-------------------------" )
        aug_index = len( self.samples ) - 1
        size = len( training_ids )
        augmented_ids = []
        for index, training_id in enumerate(training_ids):
            print(  "Augmenting data - " + str( math.floor(((index + 1 ) / size ) * 100)) + "%", end="\r" )
            if ( random.uniform(0, 1) >= 1.0 - augmentation_probability ):
                self.samples.append([self.samples[training_id][0], self.samples[training_id][1], torch.tensor(self.feature_engineering_augmented(self.samples[training_id][0])).float()])
                aug_index += 1
                augmented_ids.append( aug_index )
        training_ids += augmented_ids
        return training_ids

    def set_training(self, training):
        self.training = training

    def feature_engineering_cached(self, filename, rebuild_cache=False):
        cached_filename = filename + "_fe";
        if (os.path.isfile(cached_filename) == False or rebuild_cache == True):
            data_row = training_feature_engineering(filename, self.settings)
            np.savetxt( cached_filename, data_row )
        
        return np.loadtxt( cached_filename, dtype='float' )
        
    def feature_engineering_augmented(self, filename):
        return augmented_feature_engineering(filename, self.settings)
                    
    def __len__(self):
        return len( self.samples )

    def __getitem__(self, idx):
        #if (self.training ):
        #    return self.augmented_samples[idx][2], self.augmented_samples[idx][1]
        #else :
        return self.samples[idx][2], self.samples[idx][1]
		
    def get_labels(self):
        return self.paths
