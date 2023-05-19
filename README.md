# MatchVNE: A Stable Virtual Network Embedding Strategy Based on Matching Theory

## Execution Environment:

Operation System: Microsoft Windows 10, 64bit.<br />
Physical Memory (RAM) 16.0 GB.<br />


### Prerequisites

Python 3.9.<br />
PyCharm Community Edition 2021.2. <br />
Alib utility for VNE simulation.<br />
Introduction about VNE prblem can be found in below link:<br />
https://www.youtube.com/watch?v=JKB3aVyCMuo&t=506s<br />

### Installation

###  Download the ALIB_Utility tool unzip and copy it to the execution drive.<br /> 

- Configure the alib by following the steps mentioned in the github reposotory [1]. <br />

- Generate the input.pickle file and save it in the P3_ALIB_MASTER\input path. <br />

- Make sure "P3_ALIB_MASTER\input" path contain senario_RedBestel.pickle. If not, generate the substrate network scenario for "senario_RedBestel.pickle" in folder P3_ALIB_MASTER\input and this pickle file contains substrate network information.<br />

###   Download  MatchVNE and keep it in the drive where P3_ALIB_MASTER is present. The  MatchVNE  file contains all executable files related to the proposed and baseline approaches. <br />

- DAA.py -> The Main file related to the proposed MatchVNE approach.<br />

- greedy.py -> The Main file related to the VNE-MWF baseline approach.<br />

- Rethinking.py ->  The Main file related to the  DPGA baseline approach [2].<br />

## Usage

###  In vne_u.py, we can set the various parameters related to Virtual network requests(VNRs).<br />

- We can set the minimum and maximum number of VMs of VNRs in the create_vne function.<br />

- We can set the virtual network request demands like BandWidth(min, max), CRB(min, max), LocationX(min, max), LocationY(min, max), and Delay(min, max) in vne. append function. <br />
- Example: (1, 5, 1, 10, 0, 100, 0, 100, 1, 4)<br />

- Run vne_u.py after doing any modifications. <br />

###  In grpah_extraction_uniform.py:<br />

- In the get_graphs function mention the pickle file related to substrate network generation, the same is available in the folder P3_ALIB_MASTER. EX: os.path.join( os.path.dirname(current), "P3_ALIB_MASTER", "input", "senario_RedBestel.pickle",)<br />

- In graph.parameters function set substrate network resources like BandWidth(min,max), CRB(min,max), LocationX(min,max), LocationY(min,max), Delay(min,max).<br />
- Example: (500, 1000, 200, 1000, 0, 100, 0, 100, 1, 1)<br />

- Run grpah_extraction_uniform.py after doing any modification. <br />

###  In the automate.py file set the VNR size such as [250, 500, 750, 1000] and also mention the number of iterations needs to execute for each VNR size in the iteration variable.<br />

- Finally, run the automate.py file. After successfully running, a 1_uniform.pickle file is created (If it already does not exist in the specified path). It has all input parameters related to the substrate network parameters, such as CRB, Bandwidth, Delay, and Location.

- Final embedding results are captured in Results.xlsx, which includes values for various metrics for all test scenarios for every iteration.

### References
[1] E. D. Matthias Rost, Alexander Elvers, “Alib,” https://github.com/vnep-approx/alib, 2020. <br />
<br />
[2] Nguyen, Khoa TD, Qiao Lu, and Changcheng Huang. "Rethinking virtual link mapping in network virtualization." In 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall), pp. 1-5. IEEE, 2020.<br />

## Contributors
- Mr. Keerthan Kumar T G<br />
https://scholar.google.com/citations?user=fW7bzK8AAAAJ&hl=en <br />
- Dr. anurag satpathy<br />
https://anuragsatpathy.github.io/<br />
- Dr. Sourav kanti addya<br />
https://souravkaddya.in/<br />
- Dr Shashidhar G Koolagudi <br />
https://scholar.google.co.in/citations?user=WAyKHHwAAAAJ&hl=en <br />

## Citation & Acknowledgements
This codebase is available publicly for only for non-commercial use. If you use this code or any content in your research or wish to refer to the baseline models published in the README, please cite the work as:

@INPROCEEDINGS{10041377,<br />
  author={T G, Keerthan Kumar and Srivastava, Ankit and Satpathy, Anurag and Addya, Sourav Kanti and Koolagudi, S. G},<br />
  booktitle={2023 15th International Conference on COMmunication Systems & NETworkS (COMSNETS)},<br /> 
  title={MatchVNE: A Stable Virtual Network Embedding Strategy Based on Matching Theory}, <br />
  year={2023},<br />
  volume={},<br />
  number={},<br />
  pages={355-359},<br />
  doi={10.1109/COMSNETS56262.2023.10041377}}<br />


## Paper Links
- https://www.sciencedirect.com/science/article/pii/S1389128623001068
- https://ieeexplore.ieee.org/document/10041377

## Contact

If you have any questions, simply write a mail to  Keerthanswamy(AT)gmail(DOT)com.

