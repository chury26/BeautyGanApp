#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np


# In[2]:


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('../models/shape_predictor_5_face_landmarks.dat')


# In[3]:


img = dlib.load_rgb_image('../imgs/12.jpg')
plt.figure(figsize=(16,10))
plt.imshow(img)
plt.show()


# In[4]:


img_result = img.copy()
dets = detector(img, 1)  #img의 얼굴을 찾아줌, 여러개면 여러값
if len(dets) == 0: #사진에 이미지가 없을 경우
    print('cannot find faces!')
    
else: 
    fig, ax = plt.subplots(1, figsize=(16,10))
    for det in dets: 
        x, y, w, h = det.left(), det.top(), det.width(), det.height()
        rect = patches.Rectangle((x,y),w,h,linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    ax.imshow(img_result)
    plt.show()


# In[5]:


fig, ax = plt.subplots(1, figsize=(16,10))
objs = dlib.full_object_detections()
for detection in dets:
    s = sp(img, detection)
    objs.append(s)
    for point in s.parts():
        circle = patches.Circle((point.x, point.y), radius=3, edgecolor='r', facecolor='r')       
        ax.add_patch(circle)
ax.imshow(img_result)


# In[6]:


faces = dlib.get_face_chips(img, objs, size=256, padding=0.3)
fig, axes = plt.subplots(1, len(faces)+1 , figsize=(20,16))
axes[0].imshow(img)
for i, face in enumerate(faces):
    axes[i+1].imshow(face)


# In[7]:


#눈에 찍힌 네개의 점이 최대한 수평이 되도록 정렬
def align_faces(img):
    dets = detector(img,1) #얼굴을 찾음
    objs = dlib.full_object_detections()  #객체를 찾아줌 (사람/고양이 등등)
    for detection in dets:
        s = sp(img, detection)
        objs.append(s)
    faces = dlib.get_face_chips(img, objs, size= 256, padding=0.35) #padding왜 0.35? ->얼굴 det된것에서 +0.35 더 보려고
    return faces
test_img = dlib.load_rgb_image('../imgs/12.jpg')
test_faces = align_faces(test_img)  
fig, axes = plt.subplots(1, len(test_faces)+1, figsize=(20,16)) #하나의 피규어에 subplot하나
axes[0].imshow(test_img)
for i, face in  enumerate(test_faces):
    axes[i+1].imshow(face)


# In[8]:


sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.import_meta_graph('../models/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('../models'))
graph = tf.get_default_graph()
X = graph.get_tensor_by_name('X:0')
Y = graph.get_tensor_by_name('Y:0')
Xs = graph.get_tensor_by_name('generator/xs:0')


# In[15]:


def preprocess(img):
    return (img/225 - 0.5) *2    # +0.5하니까 밝기가 밝아져서? 화장이 날라감?;;

def deprocess(img):
    return (img+1) /2


# In[16]:


img1 = dlib.load_rgb_image('../imgs/12.jpg')
img1_faces = align_faces(img1)

img2 = dlib.load_rgb_image('../imgs/makeup/vFG56.png')
img2_faces = align_faces(img2)

fig, axes = plt.subplots(1,2,figsize=(16,10))
axes[0].imshow(img1_faces[0])
axes[1].imshow(img2_faces[0])
plt.show()


# In[17]:


src_img = img1_faces[0]
ref_img = img2_faces[0]

X_img = preprocess(src_img)
X_img = np.expand_dims(X_img, axis=0)

Y_img = preprocess(ref_img)
Y_img = np.expand_dims(Y_img, axis=0)

output = sess.run(Xs, feed_dict={X:X_img, Y:Y_img})
output_img = deprocess(output[0])

fig, axes = plt.subplots(1, 3, figsize=(20,10))
axes[0].set_title('Source')
axes[0].imshow(src_img)
axes[1].set_title('Reference')
axes[1].imshow(ref_img)
axes[2].set_title('Result')
axes[2].imshow(output_img)
plt.show()


# In[ ]:





# In[ ]:




