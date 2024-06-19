import os
import pathlib
import py_compile
import shutil
import zipfile
from multiprocessing.pool import ThreadPool as Pool
from time import perf_counter

import python_minifier

compiledFiles = []


def pathLeaf(path) -> str:
    return str(os.path.split(path)[1])


def bundle(srcDirectory: str, outputDirectory: str, compressionLevel: int) -> None:
    """Creates a bundle from all python files in a directory

    Args:
        srcDirectory (str): The original python file directory
        outputDirectory (str): The output directory for the bundle
        compressionLevel (int): The level of compression from 0 to 9
    """

    shutil.rmtree(outputDirectory)  # Deletes current contents of output directory
    shutil.copytree(srcDirectory, outputDirectory)  # Copies source to output directory

    pythonFiles = [
        str(entry).replace(os.sep, "/")  # Appends a string of the file path with forward slashes
        for entry in pathlib.Path(outputDirectory).iterdir()  # For all the file entries in the directory
        if ".py" in str(pathlib.Path(entry))
    ]  # If it is a verified file and is a python file
    # Below is where the compiling and optimizations happen
    if MULTIPROCESSING == "True" and (MINIFICATION == "True" or BYTECODECOMPILATION == "True"):
        pool = Pool(MULTIPROCESSINGPOOLS) # 6 is the pool size
        for file in pythonFiles:
            pool.apply_async(
                compileAndMinify,
                (
                    file,
                    outputDirectory,
                ),
            )
        pool.close()
        pool.join()
    elif MULTIPROCESSING == "False":
        for file in pythonFiles:
            if MINIFICATION == "True" or BYTECODECOMPILATION == "True":
                compileAndMinify(file, outputDirectory)
            else:
                compiledFiles.append(file, outputDirectory)
    with zipfile.ZipFile(f"{outputDirectory}bundle.py", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=compressionLevel) as bundler:
        for file in compiledFiles:
            bundler.write(file, arcname=pathLeaf(file))  # pathleaf is needed to not maintain folder structure
            os.remove(file)  # Clean up


def compileAndMinify(file: str, outputDirectory: str) -> None:
    """Compiles and minifies python files

    Args:
        file (str): File name/path
        outputDirectory (str): The path for the output file to be located
    """
    with open(file, "r+") as fileRW:
        if MINIFICATION == "True":
            minifiedCode = python_minifier.minify(fileRW.read(), rename_locals=False, rename_globals=False)  # I don't rename vars as that could cause problems when importing between files
            fileRW.seek(0)
            fileRW.writelines(minifiedCode)
            fileRW.truncate()  # This line and the seek one somehow fix some corruption issues
        if BYTECODECOMPILATION == "True":
            if "__main__" not in file:  # If the __main__.py file is found in the list ignore compilation (this is to avoid the interpreter finding no entrypoint)
                compiledFile = f"{outputDirectory}{pathLeaf(file)}c"
                py_compile.compile(file, cfile=compiledFile, optimize=2)
                os.remove(file)
                compiledFiles.append(compiledFile)  # Outputs compiled python file
            else:
                compiledFiles.append(file)  # This is only for the __main__.py file
        else:
            compiledFiles.append(file)

def unpackCfg(cfgFile: str) -> dict[str, str]:  # This is gonna assume that the the headers of the table are vertical
    """Turns a config file into a dictionary

    Args:
        cfgFile (str): Path to the config file

    Returns:
        Dict[str, str]: The config file as a dictionary with the keys being the first column and the other column being the
    """
    with open(cfgFile) as cfgContents:
        return dict([line.split("=", 1) for line in [line.strip("\n") for line in cfgContents if line.strip() != ""]])  # The if is needed due to a bug where the process would fail due to an empty line in the config


if "__main__" in __name__:
    
    cfg = unpackCfg("tinyBundle.cfg")
    SOURCEDIRECTORY = cfg.get("sourceDirectory")
    OUTPUTDIRECTORY = cfg.get("outputDirectory")
    COMPRESSIONLEVEL = int(cfg.get("compressionLevel"))
    
    MULTIPROCESSING = cfg.get("multiprocessing")
    MULTIPROCESSINGPOOLS = int(cfg.get("multiprocessingPools"))
    
    MINIFICATION = cfg.get("minification")
    BYTECODECOMPILATION = cfg.get("bytecodeCompilation")
    
    start = perf_counter()
    if not os.path.exists(OUTPUTDIRECTORY):
        os.makedirs(OUTPUTDIRECTORY)
    bundle(SOURCEDIRECTORY, OUTPUTDIRECTORY, COMPRESSIONLEVEL)
    end = perf_counter()

    print(f"Bundled in {end - start} seconds")