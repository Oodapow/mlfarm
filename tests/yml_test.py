import mlfarm.visitors.core
import mlfarm.visitors.files
import os
import yaml

def test():
    file = os.path.abspath(os.path.join(__file__, '..', 'assets', 'yml', 'test.yml'))

    tf = mlfarm.visitors.core.CompositeVisitor(
        mlfarm.visitors.files.YMLLoadVisitor(),
        mlfarm.visitors.core.ClassVisitor()
    )

    vtf = tf.visit(file)

    file = os.path.abspath(os.path.join(__file__, '..', 'assets', 'yml', 'a.yml'))

    res = vtf.visit(file)
    
    print(res)

if __name__ == "__main__":
    test()