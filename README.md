# ⚡️ Data ⚡️

## ⚡️ Set 1 – breast cancer (10k samples)

- 5000 images for benign  
- 5000 images for malignant  
- 512 × 512 images, jpg  
- high variance, seems work-able though  
https://www.kaggle.com/datasets/obulisainaren/multi-cancer

this may be the best choice, because  
it will perform well with a well-trained CNN  

> **Primary task**  
> • Binary image classification: benign vs malignant  
>
> **Secondary tasks**  
> • Model calibration (probability reliability)  
> • Feature attribution / saliency inspection  
>
> **Expected failure modes**  
> • Overfitting to stain color or scanner artifacts  
> • Poor generalization to slides from unseen labs  

---

## ⚡️ Set 2 – leukemia (20k samples)

- 5000 images for benign  
- 5000 images for early  
- 5000 images for pre  
- 5000 images for progressed  
- 512 × 512 images, jpg  
- lots of blurry, dirty, artifact rich samples  
- i estimate this would train a poorly performing model  
  https://www.kaggle.com/datasets/obulisainaren/multi-cancer

> **Primary task**  
> • Multi-class classification: benign / early / pre / progressed  
>
> **Secondary tasks**  
> • Artifact-robust feature learning  
> • Stage severity ordering (ordinal awareness)  
>
> **Expected failure modes**  
> • Model learning blur, dirt, or compression artifacts  
> • Class confusion between adjacent disease stages  

---

## ⚡️ Set 3 – blood cells (16k samples)

- ~2500 images for Lymphoblast  
- ~3000 images for Lymphocyte  
- ~2500 images for Myeloblast  
- 256 × 256 png images, they exist in 1200 × 1200  
- high variance  
https://www.kaggle.com/datasets/rashasalim/blood-smear-images-for-aml-diagnosis
https://www.cancerimagingarchive.net/collection/aml-cytomorphology_lmu/
(There are a few versions of this data set floating around, I have several.)

i estimate that it would be able to classify images  
from this data set. for example, if I split the data  
it would do well with predicting a myeloblast from this  
data set. unlikely to perform well for “drawing the boxes  
YOLO style on a random sample from outside the data set”

> **Primary task**  
> • Multi-class cell type classification  
>
> **Secondary tasks**  
> • In-distribution cell detection (centered objects)  
> • Representation learning for morphology similarity  
>
> **Expected failure modes**  
> • Failure on non-centered or multi-cell images  
> • Severe domain shift on external lab data  

---

## ⚡️ Set 4 – electro-cardiograms (> 250 data points each, 244500 "samples")

- 978 images with EKG reading and CSV file  
- images are 2200 × 1700 png  
- CSV have many readings for I, II, and III  
  https://www.kaggle.com/competitions/physionet-ecg-image-digitization/data

extremely well formatted, pre-processed data  
all the images line up, all the same markers in same places  
the EKG are hard to process due to signal overlaps  
this is Kaggle competition with cash prize  

i estimate this as 90% a pre-processing job, identifying  
how likely certain pixels are to belong to which line  

converting the pixels into signal should be straight forward  

### Lead I
- LA − RA  
- Views the heart from the left side  
- Best for lateral wall activity  
- Normally upright P, QRS, T waves  

### Lead II
- LL − RA  
- Views from the lower left  
- Aligns closely with the heart’s main electrical axis  
- Often the cleanest rhythm strip  
- Most commonly displayed continuously  

### Lead III
- LL − LA  
- Views from the lower right  
- Complements Lead II  
- Useful for inferior wall assessment  

> **Primary task**  
> • Signal reconstruction: extract clean Lead I, II, III waveforms from images  
>
> **Secondary tasks**  
> • Beat segmentation (P, QRS, T detection)  
> • Downstream rhythm classification  
>
> **Expected failure modes**  
> • Line overlap and lead crossing ambiguity  
> • Non-continuous signal leading to categorical errors  


---

## ⚡️ Set 5 – bone marrow (9800 samples, 171,000 samples)

- 1000 of each type for training for BLA, EOS, LYT, MON, NGS, NIF, PMO  
- 200 of each type for testing for BLA, EOS, LYT, MON, NGS, NIF, PMO  
- 200 of each type for validation for BLA, EOS, LYT, MON, NGS, NIF, PMO  
- another data set with 171,000 samples exists too, which I also have.

there are some dupes and what looks like portions of sequences  
radical variation in the data set  

**Cell types**
- BLA = Blast cells  
- EOS = Eosinophils  
- LYT = Lymphocytes  
- MON = Monocytes  
- NGS = Neutrophilic granulocytes (segmented)  
- NIF = Neutrophilic immature forms  
- PMO = Promonocytes  
  https://www.kaggle.com/datasets/shuvokumarbasakbd/bone-marrow-cell-colorized-classification/data

According to online knowledge, “bone marrow datasets are brutal,”  
so I expect this is going to perform poorly.  

> **Primary task**  
> • Multi-class cell lineage classification  
>
> **Secondary tasks**  
> • Lineage grouping (immature vs mature cells)  
> • Confusion-aware uncertainty estimation  
>
> **Expected failure modes**  
> • Irreducible label noise from expert disagreement  
> • Confusion between morphologically similar immature cells (PMO, NIF, BLA)  

---

## ⚡️ Set 6 – synthetic high signal virus (250k samples)

- Synthetic RGB circle-based images generated programmatically  
- Explicit 1–1 mapping between image content and labels  
- No label noise, no annotation ambiguity  
- Fully controllable distributions (size, color, position, overlap)  
- Original dataset is **not COCO format**; the new version is exported in **COCO format**  
- Dataset generated using **CircleFarmer**  
  https://github.com/nraptis/CircleFarmer  

this data set exists to remove uncertainty from the learning problem  
and isolate model behavior under ideal supervision conditions  

> **Primary task**  
> • Multi-class image classification with exact ground truth  
>
> **Secondary tasks**  
> • Controlled generalization testing (distribution shifts)  
> • Representation learning under perfect supervision  
>
> **Expected failure modes**  
> • Overfitting to trivial geometric or color cues  
> • Poor transfer to real-world, noisy medical imagery  

