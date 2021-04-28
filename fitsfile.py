# fitsfile.py
## Nathaniel Kerman
### April 12 2021
import os
from astropy.io import fits
import pandas as pd
class fitsfile:
    """
    This is a class for working with fits files. I built it mostly to teach myself OOP.
    But, it is useful for getting quick, COS-focused info on fitsfiles.
    """
    def __init__(self,filepath, verbose = False):
        self.path = filepath
        self.filename = os.path.basename(filepath)
        # Try to get the first 3 headers:
        self.prihdr = fits.getheader(filepath, ext = 0)
        self.detector = self.prihdr['DETECTOR']
        if self.detector == 'FUV':
            self.lppos = self.prihdr['LIFE_ADJ']
        else:
            try:
                self.lppos = self.prihdr['LIFE_ADJ']
            except:
                self.lppos = None
        try: # Not every file has a SEGMENT
            self.seg = self.prihdr.get('SEGMENT')
        except KeyError:
            self.seg = None
        self.instrument = self.prihdr.get('INSTRUME')
        self.grating = self.prihdr.get('OPT_ELEM')
        self.cenwave = self.prihdr.get('CENWAVE')
        self.obsmode = self.prihdr.get('OBSMODE')
        self.obstype = self.prihdr.get('OBSTYPE')
        self.exptype = self.prihdr.get('EXPTYPE')

        self.vitalstats = [self.filename,self.instrument,self.detector,
        self.grating,self.cenwave,self.lppos,self.obsmode,self.exptype]
        
        try: 
            self.hdr1 = fits.getheader(filepath, ext = 1)
            try: 
                self.hdr2 = fits.getheader(filepath, ext = 2)
                if verbose:
                    print("Wow! You even got a 2th header - good for you!!")
            except:
                if verbose:
                    print("Can't access a 2th header")
        except:
            if verbose:
                print("Can't access a 1th header")
    
    ######### METHODS ###########
    
    def check_keyval(self, keyword_, value_cond, verbose = False, ext = 0): # conditional values, i.e. what they should be
        """
        Checks an individual header's keyword value against what you specify.
        """
        try:
            test_keyval = fits.getheader(self.path, ext = ext)[keyword_]

            if test_keyval == value_cond:
                if verbose:
                    print(f"Matched conditional: {keyword_} = {test_keyval}")
                return True
            elif (type(value_cond) == str) & (value_cond == str(test_keyval)):
                if verbose:
                    print(f"Matched conditional (with wrong type): {keyword_} = {test_keyval}")
                    print(f"    Header value type = {type(test_keyval)}, dataframe values are str")
                return True
            else:
                if verbose:
                    print(f"Failed conditional keyword {keyword_}, is {test_keyval}, should be {value_cond}")
                return False
        except:
            print(f"Hmm - it doesn't seem like that keyword ({keyword_}) exists in that extension's header ({ext})")
            return False
    
    def compare_values(self, specified_data, verbose = False):
        """
        Checks a whole series of header values using check_keyval().
        Inputs: 
        specified_data can be a dict, but a pandas dataframe is better!
        dataframes allow access to other headers aside from primary header.
        """
        comparison_list = []
        if type(specified_data) == dict:
            for key,val in specified_data.items():
                comparison_list.append(self.check_keyval(key,val, verbose, ext = 0))

        elif type(specified_data) == pd.core.frame.DataFrame:
            for index, (key, val, ext) in specified_data.iterrows():
                comparison_list.append(self.check_keyval(key,val, verbose, ext))
        return comparison_list
    
    def check_keys_exist(self, keylist, verbose = False):
        """
        Checks a list of keywords to see if they exist in the file's 0th/1th header
        """
        exist_list = []
        for ch_key in keylist:
            try:
                self.prihdr[ch_key]
                exist_list.append(True)
                if verbose:
                    print(f'Key {ch_key} exists in the 0th header')
            except KeyError:
                try:
                    self.hdr1[ch_key]
                    exist_list.append(True)
                    if verbose:
                        print(f'Key {ch_key} exists in the 1th header')
                except KeyError:
                    exist_list.append(False)
                    if verbose:
                        print(f'Key {ch_key} does not exist in 0th/1th header')
        return exist_list
    
    def check_values_all_modes(self, mode_csv, verbose = False):
        """
        If FUV/LP4, then checks the exptype mode i.e. EXTERNAL/SCI  \
        then runs a compare_values with the relevant row of the     \
        mode_csv, which specifies 0th header key val pairs for each \
        exptype mode.
        """
        if (self.lppos == 4) & (self.detector == 'FUV'):
            mode_df = pd.read_csv(mode_csv, index_col=0)
            mode_row = mode_df.loc[self.exptype]
            mode_row_dict = mode_row.to_dict()
            if verbose:
                print(f"It looks like this file is a {self.exptype} , assuming the settings: ",
                  "\n"+repr(mode_row))
            ### CALL compare_values ###
            return self.compare_values(mode_row_dict,verbose = verbose)
            
        elif self.detector != 'FUV':
            if verbose:
                print("Not an FUV exposure")
        elif self.lppos < 4:
            if verbose:
                print("Not an LP4 exposure")

    default_check_key_list = ['XTRCTALG', 'TRCECORR', 'ALGNCORR']
    def run_LP4_kw_test(self, mode_csv = os.getcwd()+'/COS_Lp4_modes.csv',
                        check_key_list=default_check_key_list, verbose = False):
        """
        If fitsfile is lp4, then...
        Runs the tests in order:
        1. checks that hdr keys exist
        2. checks their values against expected values
        """
        if self.lppos == 4:
            
            ###### TEST HDR KEYS EXIST: ######

            if verbose:
                print("### 1: Testing all keys exist:")
            passed_exist_test_list = self.check_keys_exist(keylist=check_key_list, verbose=verbose)
            passed_exist_test_bool = all(passed_exist_test_list)

            ###### TEST HDR KEY VALUES ARE EXPECTED VALUES: ######
            if verbose:
                print(f"### 2: Testing all keys match those in :{mode_csv}")
            passed_value_test_list = self.check_values_all_modes(mode_csv, verbose = verbose)
            passed_value_test_bool = all(passed_value_test_list)
            
            return passed_exist_test_bool, passed_value_test_bool
