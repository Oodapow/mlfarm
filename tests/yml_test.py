import mlfarm.yml.transforms as transforms
import os

def test():
    tf = transforms.RelativeLoadTransform()

    print(tf(file_path=os.path.abspath(os.path.join(__file__, '..', 'a.yml'))))