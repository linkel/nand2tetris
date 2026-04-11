- an instance variable is a variable declared inside of a class but not in any methods. usually used to hold state. so if it's unique to that instance it's an instance variable
- this is as opposed to a class variable which would be the same for all classes of that object. so the state inside of __init__ is instance, if it was just inside the class it'd be class var. 

```python
class Dog:
    kind = 'canine'         # Class variable (shared)

    def __init__(self, name):
        self.name = name    # Instance variable (unique)
```


uh my compile subroutine call, should that be Usage.used when it hasn't even been declared?? 