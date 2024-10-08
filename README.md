
# Basic 2D/3D Vision Tasks Evaluation
*Performance measures for evaluating 2D/3D multi-object detection, segmentation and tracking.*

## Implemented Performance Measures

The following performance measures are currently implemented:

Measures | Sub-Measures |   Paper | Code | Notes |
|----- | ----------- |----- | ----------- | ----- |
| | | |  |  |
|**OSPA(2) (OSPATrack) metric**| OSPA2, OSPA2_CARD, OSPA2_LOC| [paper](https://ieeexplore.ieee.org/document/9976259)|[code](trackeval/metrics/ospa2.py)| A metric for multi-object tracking |
|**OSPA (OSPADetection) metric**| OSPA, OSPA_CARD, OSPA_LOC| [paper](https://ieeexplore.ieee.org/document/9976259)|[code](trackeval/metrics/ospa.py)| A metric for multi-object detection and segmentation |
|**HOTA**|HOTA, DetA, AssA, LocA, DetPr, DetRe, AssPr, AssRe|[paper](https://link.springer.com/article/10.1007/s11263-020-01375-2)|[code](trackeval/metrics/hota.py)| |
|**CLEARMOT**|MOTA, MOTP, MT, ML, Frag, etc.|[paper](https://link.springer.com/article/10.1155/2008/246309)|[code](trackeval/metrics/clear.py)| |
|**Identity**|IDF1, IDP, IDR|[paper](https://arxiv.org/abs/1609.01775)|[code](trackeval/metrics/identity.py)| |
|**VACE**|ATA, SFDA|[paper](https://link.springer.com/chapter/10.1007/11612704_16)|[code](trackeval/metrics/vace.py)| |
|**Track mAP**|Track mAP|[paper](https://arxiv.org/abs/1905.04804)|[code](trackeval/metrics/track_map.py)|Requires confidence scores|
|**J & F**|J&F, J, F|[paper](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Perazzi_A_Benchmark_Dataset_CVPR_2016_paper.pdf)|[code](trackeval/metrics/j_and_f.py)|Only for Seg Masks|
|**ID Euclidean**|ID Euclidean|[paper](https://arxiv.org/pdf/2103.13516.pdf)|[code](trackeval/metrics/ideucl.py)| |

Note: 
- **[Generalized Intersection over Union (GIOU)](https://openaccess.thecvf.com/content_CVPR_2019/papers/Rezatofighi_Generalized_Intersection_Over_Union_A_Metric_and_a_Loss_for_CVPR_2019_paper.pdf) is included as a base metric for bounding box evaluation. Use the 'GIOU' flag in the evaluation scripts to choose the base metric. Note that the GIOU score is normalized to values between 0 and 1, same as the IOU score.**
- OSPA(2) and OSPA metrics are given in terms of distances (errors), hence the lower the better.
- OSPA(2) and OSPA are the main distances (errors). OSPA2_CARD and OSPA_CARD are the cardinality error components, and OSPA2_LOC and OSPA_LOC are the localization error components.
- By definitions:
  -  OSPA2 = OSPA2_CARD + OSPA2_LOC,
  -  OSPA = OSPA_CARD + OSPA_LOC.

## Implemented Benchmarks

The following benchmarks are currently implemented:

Benchmark | Sub-benchmarks | Type | Website | Code | Data Format |
|----- | ----------- |----- | ----------- | ----- | ----- |
| | | |  |  | |
|**Curtin Multi-Camera**|CMC1/2/3/4/5|3D BBox|[website](https://github.com/linh-gist/3D-Visual-MOT)|[code](trackeval/datasets/cmc_3d_box.py)|[format](docs/CMC-3D-box-format.txt)|
|**RobMOTS**|Combination of 8 benchmarks|Seg Masks|[website](https://eval.vision.rwth-aachen.de/rvsu-workshop21/?page_id=110)|[code](trackeval/datasets/rob_mots.py)|[format](docs/RobMOTS-Official/Readme.md)|
|**Open World Tracking**|TAO-OW|OpenWorld / Seg Masks|[website](https://openworldtracking.github.io)|[code](trackeval/datasets/tao_ow.py)|[format](docs/OpenWorldTracking-Official/Readme.md)|
|**MOTChallenge**|MOT15/16/17/20|2D BBox|[website](https://motchallenge.net/)|[code](trackeval/datasets/mot_challenge_2d_box.py)|[format](docs/MOTChallenge-format.txt)|
|**KITTI Tracking**| |2D BBox|[website](http://www.cvlibs.net/datasets/kitti/eval_tracking.php)|[code](trackeval/datasets/kitti_2d_box.py)|[format](docs/KITTI-format.txt)|
|**BDD-100k**| |2D BBox|[website](https://bdd-data.berkeley.edu/)|[code](trackeval/datasets/bdd100k.py)|[format](docs/BDD100k-format.txt)|
|**TAO**| |2D BBox|[website](https://taodataset.org/)|[code](trackeval/datasets/tao.py)|[format](docs/TAO-format.txt)|
|**MOTS**|KITTI-MOTS, MOTS-Challenge|Seg Mask|[website](https://www.vision.rwth-aachen.de/page/mots)|[code](trackeval/datasets/mots_challenge.py) and [code](trackeval/datasets/kitti_mots.py)|[format](docs/MOTS-format.txt)|
|**DAVIS**|Unsupervised|Seg Mask|[website](https://davischallenge.org/)|[code](trackeval/datasets/davis.py)|[format](docs/DAVIS-format.txt)|
|**YouTube-VIS**| |Seg Mask|[website](https://youtube-vos.org/dataset/vis/)|[code](trackeval/datasets/youtube_vis.py)|[format](docs/YouTube-VIS-format.txt)|
|**Head Tracking Challenge**| |2D BBox|[website](https://arxiv.org/pdf/2103.13516.pdf)|[code](trackeval/datasets/head_tracking_challenge.py)|[format](docs/MOTChallenge-format.txt)|
|**PersonPath22**| |2D BBox|[website](https://github.com/amazon-research/tracking-dataset)|[code](trackeval/datasets/person_path_22.py)|[format](docs/MOTChallenge-format.txt)|
|**BURST**| {Common, Long-tail, Open-world} Class-guided, {Point, Box, Mask} Exemplar-guided |Seg Mask|[website](https://github.com/Ali2500/BURST-benchmark)|[format](https://github.com/Ali2500/BURST-benchmark/blob/main/ANNOTATION_FORMAT.md)|

## Evaluating Multi-Object Detection and Segmentation
OSPA metric (not OSPA(2)) can be used for multi-object detection/segmentation, and it can be done by:
- First, convert your data to MOTChallenge format (2D bounding box or segmentation mask), treating each image as a frame.
- In each image, assign the detected objects with distinct IDs to ensure the data pre-processing steps can be done correctly. Note that, the IDs can be reused for different images as long as in each image they are distinct.
- The OSPA metric does not use object IDs in the evaluation, which means, the distinct IDs can be generated randomly.
- Finally, use the OSPA metric (not OSPA(2)) to evaluate.

## Running the Code
The code can be run in one of two ways:

 - From the terminal via one of the scripts [here](scripts/). See each script for instructions and arguments.
 - Directly by importing this package into your code, see the same scripts above for how.

## Outputs

By default the code prints results to the screen, saves results out as both a summary txt file and a detailed results csv file, and outputs plots of the results. All outputs are by default saved to the 'tracker' folder for each tracker.

## Quick Test on Supported Benchmarks

Ground-truth data, meta-data and example trackers for all currently supported benchmarks are provided in the following link.
You can download this here: [data.zip](https://drive.google.com/file/d/1VYC6iOFyN2WAoA0JB0dzXbIlYPabC34t/view?usp=sharing) (~150mb).

The data for RobMOTS is separate and can be found here: [rob_mots_train_data.zip](https://omnomnom.vision.rwth-aachen.de/data/RobMOTS/train_data.zip) (~750mb).

The data for PersonPath22 is separate and can be found here: [person_path_22_data.zip](https://tracking-dataset-eccv-2022.s3.us-east-2.amazonaws.com/person_path_22_data.zip) (~3mb).

The easiest way to begin is to extract this zip into the repository root folder such that the file paths look like: VisionEvaluation/data/gt/...

This then corresponds to the default paths in the code. You can now run each of the scripts [here](scripts/) without providing any arguments and they will by default evaluate all trackers present in the supplied file structure. To evaluate your own tracking results, simply copy your files as a new tracker folder into the file structure at the same level as the example trackers (MPNTrack, CIWT, track_rcnn, qdtrack, ags, Tracktor++, STEm_Seg), ensuring the same file structure for your trackers as in the example.

If your ground truth and tracker files are located somewhere else, you can use the script arguments to point the code toward your data.

To ensure your tracker outputs data in the correct format, check out the format guides for each of the supported benchmarks [here](docs), or check out the example trackers provided.

## Evaluation on Custom Benchmark

To evaluate on a custom benchmark, there are two options:
 - Write custom dataset code.
 - Convert your current dataset and trackers to the same format as an already implemented benchmark.

To convert formats, check out the format specifications defined [here](docs).

By default, it is recommended to use the MOTChallenge format, although any implemented format should work. Note that for many cases you will want to use the argument ```--DO_PREPROC False``` unless you want to run preprocessing to remove distractor objects.

## Requirements
 Code tested on Python 3.7.
 
 - Minimum requirements: numpy, scipy
 - For plotting: matplotlib
 - For segmentation datasets (KITTI MOTS, MOTS-Challenge, DAVIS, YouTube-VIS): pycocotools
 - For DAVIS dataset: Pillow
 - For J & F metric: opencv_python, scikit_image
 - For simples test-cases for metrics: pytest

use ```pip3 -r install requirements.txt``` to install all possible requirements.

use ```pip3 -r install minimum_requirments.txt``` to only install the minimum if you don't need the extra functionality as listed above.

## Acknowledgement

Parts of the codes and most of the information in this README file are released under the 'TrackEval' repo by Jonathon Luiten and Arne Hoffhues at https://github.com/JonathonLuiten/TrackEval. 
Please include the following citation in your research if you use the code.

```BibTeX
@misc{luiten2020trackeval,
  author =       {Jonathon Luiten, Arne Hoffhues},
  title =        {TrackEval},
  howpublished = {\url{https://github.com/JonathonLuiten/TrackEval}},
  year =         {2020}
}
```

The OSPA(2) and OSPA metrics (and other performance criteria) for multi-object tracking, detection and segmentation evaluation are discussed in the following paper:

```BibTeX
@ARTICLE{9976259,
  author={Nguyen, Tran Thien Dat and Rezatofighi, Hamid and Vo, Ba-Ngu and Vo, Ba-Tuong and Savarese, Silvio and Reid, Ian},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence}, 
  title={How Trustworthy are Performance Evaluations for Basic Vision Tasks?}, 
  year={2023},
  volume={45},
  number={7},
  pages={8538-8552},
  doi={10.1109/TPAMI.2022.3227571}}
```

If you use any performance measures and benchmarks, please cite the relevant papers.

## Contact
Contributor: Tran Thien Dat Nguyen. Email: tranthiendat.nguyen@gmail.com
