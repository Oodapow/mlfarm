import transforms
import os

tf = transforms.RelativeLoadTransform()

print(tf(file_path=os.path.abspath(os.path.join(__file__, '..', 'a.yml'))))