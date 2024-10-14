import os
import pathlib
import shutil
import zipfile
from time import perf_counter
import python_minifier

def pathLeaf(path) -> str:
    return str(os.path.split(path)[1]).strip()


def bundle(srcDirectory: str, outputDirectory: str, compressionLevel: int) -> None:
    """Creates a bundle from all python files in a directory

    Args:
        srcDirectory (str): The original python file directory
        outputDirectory (str): The output directory for the bundle
        compressionLevel (int): The level of compression from 0 to 9
    """

    shutil.rmtree(outputDirectory)  # Deletes current contents of output directory
    shutil.copytree(srcDirectory, outputDirectory)  # Copies source to output directory

    pythonFiles: list[str] = [
        str(entry).replace(os.sep, "/")  # Appends a string of the file path with forward slashes
        for entry in pathlib.Path(outputDirectory).iterdir()  # For all the file entries in the directory
        if ".py" in str(pathlib.Path(entry))
    ]  # If it is a verified file and is a python file
    if MINIFICATION == "True":
        for file in pythonFiles:
            with open(file, "r+") as fileRW:
                minifiedCode = python_minifier.minify(fileRW.read(), 
                    rename_locals=False, 
                    rename_globals=False
                ) # I don't rename vars as that could cause problems when importing between files
                fileRW.seek(0)
                fileRW.writelines(minifiedCode)
                fileRW.truncate()
    with zipfile.ZipFile(f"{outputDirectory}bundle.py", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=compressionLevel) as bundler:
        for file in pythonFiles:
            bundler.write(file, arcname=pathLeaf(file))  # pathleaf is needed to not maintain folder structure
            os.remove(file)  # Clean up

def unpackCfg(cfgFile: str) -> dict[str, str]:  # This is gonna assume that the the headers of the table are vertical
    """Turns a config file into a dictionary

    Args:
        cfgFile (str): Path to the config file

    Returns:
        Dict[str, str]: The config file as a dictionary with the keys being the first column and the other column being the
    """
    with open(cfgFile) as cfgContents:
        return dict([line.split("=", 1) for line in [line.strip("\n") for line in cfgContents if "=" in line]])  # The if is needed due to a bug where the process would fail due to an empty line in the config


if "__main__" in __name__:
    
    cfg: dict[str, str] = unpackCfg("tinyBundle.cfg")
    SOURCEDIRECTORY: str = str(cfg.get("sourceDirectory"))
    OUTPUTDIRECTORY: str = str(cfg.get("outputDirectory"))
    COMPRESSIONLEVEL: str = int(str(cfg.get("compressionLevel")))
    MINIFICATION: str = str(cfg.get("minification"))
    if not os.path.exists(OUTPUTDIRECTORY):
        os.makedirs(OUTPUTDIRECTORY)
    start = perf_counter()
    bundle(SOURCEDIRECTORY, OUTPUTDIRECTORY, COMPRESSIONLEVEL)
    end = perf_counter()

    print(f"Bundled in {end - start} seconds")
