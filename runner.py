import rcssmin
import rjsmin
import sass

# Map scss source files to css destination files
sass_map = {"app/static/scss/style.scss": "app/static/css/style.css"}

# Map un-minified css source files to minified css destination files
css_map = {"app/static/css/style.css": "app/static/css/style.min.css"}

# Map un-minified JavaScript source files to minified JavaScript destination files
js_map = {"app/static/js/app.js": "app/static/js/app.min.js"}


def compile_sass_to_css(sass_map):

    print("Compiling scss to css:")

    for source, dest in sass_map.items():
        with open(dest, "w") as outfile:
            outfile.write(sass.compile(filename=source))
        print(f"{source} compiled to {dest}")


def minify_css(css_map):

    print("Minifying css files:")

    for source, dest in css_map.items():
        with open(source, "r") as infile:
            with open(dest, "w") as outfile:
                outfile.write(rcssmin.cssmin(infile.read()))
        print(f"{source} minified to {dest}")


def minify_javascript(js_map):

    print("Minifying JavaScript files:")

    for source, dest in js_map.items():
        with open(source, "r") as infile:
            with open(dest, "w") as outfile:
                outfile.write(rjsmin.jsmin(infile.read()))
        print(f"{source} minified to {dest}")


if __name__ == "__main__":
    print()
    print("Starting runner")
    print("--------------------")
    compile_sass_to_css(sass_map)
    print("--------------------")
    minify_css(css_map)
    print("--------------------")
    minify_javascript(js_map)
    print("--------------------")
    print("Done")
    print()
