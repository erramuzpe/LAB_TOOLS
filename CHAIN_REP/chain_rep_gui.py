#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:55:04 2015

@author: asier
"""

# -*- coding: utf-8 -*-
import re
import wx
import os
import sys



#mystr = "I want to Remove all white \t spaces, new lines \n and tabs \t"
#print re.sub(r"\W", "", mystr)

bases = ['T', 'C', 'A', 'G']
codons = [a+b+c for a in bases for b in bases for c in bases]
amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
codon_table = dict(zip(codons, amino_acids))
codon_change_to_V = {
		"GCA" : "GTA",
		"GCC" : "GTC",
		"GCG" : "GTG",
		"GCT" : "GTT"
	}
codon_change_to_A = { #GCA GCC GCG GCT
    "TTT":"GCT", "TTC":"GCC", "TTA":"GCA", "TTG":"GCG",
    "TCT":"GCT", "TCC":"GCC", "TCA":"GCA", "TCG":"GCG",
    "TAT":"GCT", "TAC":"GCC", "TAA":"GCA", "TAG":"GCG",
    "TGT":"GCT", "TGC":"GCC", "TGA":"GCA", "TGG":"GCG",
    "CTT":"GCT", "CTC":"GCC", "CTA":"GCA", "CTG":"GCG",
    "CCT":"GCT", "CCC":"GCC", "CCA":"GCA", "CCG":"GCG",
    "CAT":"GCT", "CAC":"GCC", "CAA":"GCA", "CAG":"GCG",
    "CGT":"GCT", "CGC":"GCC", "CGA":"GCA", "CGG":"GCG",
    "ATT":"GCT", "ATC":"GCC", "ATA":"GCA", "ATG":"GCG",
    "ACT":"GCT", "ACC":"GCC", "ACA":"GCA", "ACG":"GCG",
    "AAT":"GCT", "AAC":"GCC", "AAA":"GCA", "AAG":"GCG",
    "AGT":"GCT", "AGC":"GCC", "AGA":"GCA", "AGG":"GCG",
    "GTT":"GCT", "GTC":"GCC", "GTA":"GCA", "GTG":"GCG",
    "GAT":"GCT", "GAC":"GCC", "GAA":"GCA", "GAG":"GCG",
    "GGT":"GCT", "GGC":"GCC", "GGA":"GCA", "GGG":"GCG"
	}
 

        
def chain_rep(chain,start):
    
    global codon_table
    
    codon=chain[start:start+3]
    if codon_table[codon] == 'A': #substitute for V
        codon = codon_change_to_V[codon]
    else: #substitute for A
        codon = codon_change_to_A[codon]
    chain = chain[:start] + codon + chain[start+3:]
    return chain

def reverseComplement(seq):
  sequence = seq*1
  complement = {'A':'T','C':'G','G':'C','T':'A','N':'N'}
  return "".join([complement.get(nt, '') for nt in sequence[::-1]])

def format_chain(seq,start):
    seq = seq[0:start]+" "+ \
    " ".join(seq[i:i+3] for i in range(start, len(seq)-start, 3)) \
    +" "+ seq[len(seq)-start:]
    return seq


#Main start
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.dirname=''

        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(300,20), size=(375,220), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Open button
        self.buttonopen =wx.Button(self, label="Open", pos=(20, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClickOpen,self.buttonopen)
        
        # Run button
        self.buttonrun =wx.Button(self, label="Run", pos=(110, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClickRun,self.buttonrun)
        
        # Exit button
        self.buttonexit =wx.Button(self, label="Exit", pos=(200, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClickExit,self.buttonexit)


        # the position control 
        self.lblpos = wx.StaticText(self, label="Position you would like to start", pos=(20,20))
        self.editpos = wx.TextCtrl(self, value="1", pos=(20, 45), size=(140,-1))

        # the oligo num control
        self.lbloligo = wx.StaticText(self, label="Length of oligos:", pos=(20, 80))
        self.editoligo = wx.TextCtrl(self, value="7", pos=(20, 105), size=(140,-1))
        
        # the oligo num control
        self.lblline = wx.StaticText(self, label="Line to start in the output:", pos=(20, 140))
        self.editline = wx.TextCtrl(self, value="1", pos=(20, 165), size=(140,-1))

        


    def OnClickOpen(self,event):
        global seq
        
        try:
            
            """ Open a file"""
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                #self.control.SetValue(f.read())
                seq = f.read()
                f.close()
            dlg.Destroy()
            self.logger.AppendText('File loaded! \n')   
             
             
            # seq initial treatment
            seq = re.sub(r'\W', '', seq) #remove all spaces/blanks/newlines
            seq = re.sub('[^a-zA-Z]', '', seq)  #remove all non LETTER char
            seq = seq.upper()
            self.logger.AppendText('Your chains first 20:\n %s \n' % seq[0:20])
            
            
            
        except: self.logger.AppendText("There was some problem opening the file \n")
        

    def OnClickRun(self,event):
        global seq
        
        try:        
            start_pos = int(self.editpos.GetValue())
            
            start_pos -= 1
            self.logger.AppendText('You selected %s as your starting point \n' % seq[start_pos:start_pos+10])

            seq=seq[start_pos:] #delete the rest of the chain
            
            self.logger.AppendText('Your chain now is %s ... \n' % seq[:10])
            
            
                        
            
            oligo_assert = False
            try:
                oligo_num = int(self.editoligo.GetValue())
                side_num = 0
                
                if (oligo_num-3)%2 != 0 or (oligo_num-3) <= 0: 
                    self.logger.AppendText('Incorrect number of oligos, insert a correct one \n')
                else:
                    self.logger.AppendText('Number of oligos accepted \n')

                    oligo_assert = True
                    side_num = (oligo_num-3)/2   
            except:
                self.logger.AppendText( 'Insert a number, please \n')

            if oligo_assert == True:
                
                #codon_num = (oligo_num - 3 - 2*side_num) / 2 / 3
                
                line_num = int(self.editline.GetValue())

                fname = "new_chain.txt"
                file = open(fname, 'w')
                
                
                self.logger.AppendText('\nProcessing...  \n')
                for x_ in xrange(0, len(seq), 3):
                    
                    chain = seq[x_: x_+oligo_num] 
                      
                    if len(chain) != oligo_num: break
                    
                    chain = chain_rep(chain,side_num)
                    chain_rev = reverseComplement(chain)    
                    
                    file.write(str(line_num) + " " + chain + '\n')
                    file.write(str(line_num+1) + " " + chain_rev + '\n \n')
                    
                    line_num += 2
                
                file.close()
                self.logger.AppendText('\nFinished! Results in new_chain.txt\n')
        
        except:
            self.logger.AppendText("Not file loaded? \n") 
            print "Unexpected error:", sys.exc_info()[0]
            
    
    def OnClickExit(self,event):
        app.Destroy()

app = wx.App(False)
frame = wx.Frame(None,0,'Chain Rep', size=(700,280))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()




        
        
        
           









