import pyautogui
import time

i=1
a = 0
#while for the infinite loop for mouse to run
while i:
    try:
        pyautogui.moveTo(200, 100)
        time.sleep(100)
        pyautogui.moveTo(100, 600)
        time.sleep(100)
        pyautogui.moveTo(600, 900)
        time.sleep(100)

        a += 1
        print("Iterations = ",a)
    except:
        print('Exception')


# In[22]:


pyautogui.size()


# In[23]:


pyautogui.moveTo(10, 10)