from enum import Enum, auto


class AccessType(Enum):
    READ = 'READ'
    WRITE = 'WRITE'
    MODIFY = 'MODIFY'
    DELETE = 'DELETE'

    def to_string(self):
        return self.value


class AccessHierarchy(Enum):
    DELETE = [auto(), AccessType.DELETE, AccessType.MODIFY, AccessType.WRITE, AccessType.READ]
    MODIFY = [auto(), AccessType.MODIFY, AccessType.WRITE, AccessType.READ]
    WRITE = [auto(), AccessType.WRITE, AccessType.READ]
    READ = [auto(), AccessType.READ]