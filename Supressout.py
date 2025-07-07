import os 
import contextlib


#Helper function to clead up longer logs 
@contextlib.contextmanager
def suppress_output():
    """"Supress stout and stderr including child processess"""
    with open(os.devnull, "w") as devnull:
        #Save actual file descriptors
        old_stdout_fd = os.dup(1)
        old_stderr_fd = os.dup(2)
        #Redirect stdout and stderr to /dev/null
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
        try:
            yield
        finally:
            #Restore original file descriptors
            os.dup2(old_stdout_fd, 1)
            os.dup2(old_stderr_fd, 2)
            #Close old file descriptors
            os.close(old_stdout_fd)
            os.close(old_stderr_fd)
                