class HanoiBiggerDiskError(Exception):
    '''
    Custom exception for handling Rod class error when a disk to put is larger than the top
    '''
    def __init__(self, message = ''):
        self.message = message
        super().__init__(self.message)

class HanoiNoDiskError(Exception):
    '''
    Custom exception for handling Rod class error when there are no disks and the taking function is called
    '''
    def __init__(self, message = ''):
        self.message = message
        super().__init__(self.message)

class Rod:
    '''
    Class for implementing the Tower of Hanoi rods
    '''
    # Init method
    def __init__(self, disks = []):
        for disk in disks:
            self.put_disk(disk)
        if len(disks) == 0:
            self.disks = []
    
    # Dunder methods
    def __str__(self):
        return str(self.disks)
    
    def __len__(self):
        return len(self.disks)
    
    # Class functions
    def put_disk(self, disk):
        if not hasattr(self, 'disks'):
            # If there is no list...
            self.disks = [disk]
            # ...we create it with the setter
            return
        if self.is_empty:
            # In this case there is no top.
            # Without this, it crashes in empty rods
            self.disks.append(disk)
            return
        top_disk = self.top
        if disk > top_disk:
            raise HanoiBiggerDiskError('cannot put a bigger disk on the top of the rod')
        self.disks.append(disk)
    
    def take_disk(self):
        if self.is_empty:
            raise HanoiNoDiskError('there is no disk to take')
        return self.disks.pop()
    
    def move(self, rod):
        # 'rod' is the destination rod. As there is just
        # one top disk, we don't have to ask for the
        # disk.
        if not isinstance(rod, Rod):
            raise TypeError('target rod must be instance of Rod')
        disk = self.take_disk()
        rod.put_disk(disk)
    
    def can_move(self, rod):
        # It's for checking!
        if not isinstance(rod, Rod):
            raise TypeError('rod for checking must be instance of Rod')
        if self.is_empty:
            return False
        elif rod.is_empty:
            return True
        elif self.top < rod.top:
            return True
        else:
            return False
    
    # Getters and setters
    @property
    def disks(self):
        return self.__disks
    @disks.setter
    def disks(self, new_value):
        if not isinstance(new_value, list):
            raise TypeError('disks must be a list')
        self.__disks = new_value
    
    @property
    def top(self):
        if not len(self):
            return 0
        return self.disks[-1]
    @top.setter
    def top(self, new_value):
        raise TypeError('cannot set the top directly')
        # I feel this setter is kinda troll ☉‿⚆
    
    @property
    def bottom(self):
        if not len(self):
            return 999
        return self.disks[0]
    
    @property
    def is_empty(self):
        return len(self) == 0
    @is_empty.setter
    def is_empty(self, new_value):
        raise TypeError('cannot set if the rod is empty directly')

def hanoi_solver(disks):
    if not isinstance(disks, int):
        raise TypeError("the amount of 'disks' must be an integer")
    if disks < 1:
        raise ValueError('amount of disks must be greater than 0')
    
    # Reversed order
    rod1 = Rod([n for n in range(disks, 0, -1)])
    rod2 = Rod()
    rod3 = Rod()

    moves = 0
    traceback = f'{rod1} {rod2} {rod3}'
    # Here I try to follow the pattern of the examples
    while len(rod3) < disks:
        if (len(rod1) <= 1 or rod2.is_empty or rod3.is_empty) and (rod3.top % 2 == 0 or rod3.top == 3) and (rod3.bottom % 2 == 1 or rod3.bottom == 4) and rod2.bottom != 5 and not 1 in rod3.disks and (not len(rod1) == len(rod2) == len(rod3)) and rod3.bottom != 1 and len(rod1) != 2 and len(rod1) != 4 and not (len(rod2) == 1 and rod2.top == 2) and rod1.can_move(rod3): # Most common operation
            # Ha! Sure ChatGPT couldn't have done this!
            rod1.move(rod3)
        elif ((disks == 2 and len(rod1) == 2) or ((rod3.top <= 1 or rod3.top == 3) and (rod2.is_empty or len(rod2) == 2) and rod1.bottom != 1 and rod2.bottom != 1 and rod2.bottom != 2 and rod2.bottom != 5 and (rod3.is_empty or rod3.top == 1 or rod3.top == 3))) and rod1.can_move(rod2): # Second most common
            rod1.move(rod2)
        elif len(rod1) <= 3 and (len(rod2) == 1 or len(rod2) == 3) and rod3.top != 1 and rod2.can_move(rod3): # Second most common
            rod2.move(rod3)
        elif (not (rod1.is_empty or rod2.is_empty or rod3.is_empty)) and rod3.top < 4 and (len(rod3) == 1 or (disks == 5 and len(rod3) == 2) or (len(rod3) == 3 and rod3.bottom == disks or (disks == 5 and rod3.bottom == 3))) and (len(rod2) == 1 or (len(rod2) == 3 and rod2.bottom == 4)) and len(rod1) <= 3 and rod3.can_move(rod2): # Fourth most common
            rod3.move(rod2)
        elif (not rod1.is_empty) and (not rod2.is_empty) and (not rod3.is_empty) and rod3.top <= 2 and rod3.bottom > 1 and rod2.bottom >= 3 and rod2.bottom <= 4 and rod3.can_move(rod1): # Fifth most common
            rod3.move(rod1)
        elif not (rod2.is_empty or rod3.is_empty) and len(rod1) <= 2 and rod1.top % 2 == 0 and rod2.top <= 3 and rod2.bottom >= 2 and rod3.top != 2 and rod3.top != 4 and ((len(rod3) == 1 and (rod3.top == 3 or rod3.top == 5)) or (len(rod3) >= 2 and len(rod3) <= 3)) and rod2.can_move(rod1): # Third most common (it gave problems...)
            rod2.move(rod1)
        
        traceback += f'\n{rod1} {rod2} {rod3}'
        moves += 1
        if moves >= 2 ** disks - 1:
            break
    
    return traceback
