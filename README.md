# What is this?

tinyBundle is a bundler which compresses multiple python files into a single file!

This is similar to [pyz](https://github.com/BTOdell/pyz) and [zipapp](https://docs.python.org/3/library/zipapp.html) but doesn't require its own file type, hence it acts more like JavaScript's [rollup](https://rollupjs.org/).

# How do I install the project?

You can either click the 'Use this template' button in Github or using git you can perform a git clone

    git clone https://github.com/jakewdr/tinyBundle

Then you need to install [make](https://www.gnu.org/software/make/#download) on the relevant platform

Finally to install dependencies run:

    make setup

# How do I build a bundle?

To build a bundle just run:

    make build

To build and run a bundle enter:

    make run

# Example project

~~I've made a simple project which checks a image's file size here to give an example of what tinyBundle can do, you can find that [here](https://github.com/jakewdr/imageFileSizeChecker).~~
