# MatchVNE
Execution Environment: <br />
Operation System: Microsoft Windows 10, 64bit.<br />
Physical Memory (RAM) 16.0 GB.<br />
Python 3.9. PyCharm Community Edition 2021.2. Alib utility for VNE simulation.<br />

Introduction about VNE prblem can be found in below link:
https://www.youtube.com/watch?v=JKB3aVyCMuo&t=506s



Step 1: Download the ALIB_Utility tool [1] (alib utility in par with python 2.7) and copy it to the execution drive. <br />
1a. Configure the alib by following the steps mentioned in the link(https://github.com/vnep-approx/alib).<br />
1b. Generate the input.pickle file and save it in the P3_ALIB_MASTER\input path. 1b. Make sure "P3_ALIB_MASTER\input" path contain senario_RedBestel.pickle. If not, generate the substrate network scenario for senario_RedBestel in folder P3_ALIB_MASTER\input and this pickle file contains substrate network information.<br />

Step 2: Download  MatchVNE and keep it in the drive where P3_ALIB_MASTER is present. The  MatchVNE  file contains all executable files related to the proposed and baseline approaches. <br />
DAA.py -> The Main file related to the proposed MatchVNE approach.<br />
greedy.py -> The Main file related to the VNE-MWF baseline approach.<br />
Rethinking.py ->  The Main file related to the  DPGA baseline approach [2].<br />

Step 3: In vne_u.py, we can set the various parameters related to Virtual network requests(VNRs).<br />

3a. We can set the minimum and maximum number of VMs of VNRs in the create_vne function.<br />

3b. We can set the virtual network request demands like BandWidth(min, max), CRB(min, max), LocationX(min, max), LocationY(min, max), and Delay(min, max) in vne. append function. EX: (1, 5, 1, 10, 0, 100, 0, 100, 1, 4)<br />

3c. Run vne_u.py after doing any modifications. Step 4: In grpah_extraction_uniform.py:<br />

4a. In the get_graphs function mention the pickle file related to substrate network generation, the same is available in the folder P3_ALIB_MASTER. EX: os.path.join( os.path.dirname(current), "P3_ALIB_MASTER", "input", "senario_RedBestel.pickle",)<br />

4b. In graph.parameters function set substrate network resources like BandWidth(min,max), CRB(min,max), LocationX(min,max), LocationY(min,max), Delay(min,max). Ex: (500, 1000, 200, 1000, 0, 100, 0, 100, 1, 1)<br />

4c. Run grpah_extraction_uniform.py after doing any modification. <br />

Step 5: In the automate_c1.py file set the VNR size such as [250, 500, 750, 1000] and also mention the number of iterations needs to execute for each VNR size in the iteration variable.<br />

Step 6: Finally run the automate_c1.py file. After successfully running a 1_uniform.pickle file is created and it is having all input parameters related to both substrate network and Virtual network request parameters and final embedding results are captured in the Results.xlsx.  

References:<br />
[1] E. D. Matthias Rost, Alexander Elvers, “Alib,” https://github.com/vnep-approx/alib, 2020. <br />
<br />
[2] Nguyen, Khoa TD, Qiao Lu, and Changcheng Huang. "Rethinking virtual link mapping in network virtualization." In 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall), pp. 1-5. IEEE, 2020.<br />

