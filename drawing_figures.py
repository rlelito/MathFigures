import figures
import inspect

figures_list = []
for name, obj in inspect.getmembers(figures):
    if inspect.isclass(obj) and obj.__module__ == 'figures' and obj.__name__ != 'ConvexPolygon':
        figures_list.append(obj)

print("Figures list to choose:")
for index, value in enumerate(figures_list):
    print(f"{index:2}) {value.__name__}")

opt = int(input('>>> '))

chosen = figures_list[opt].user_input()
chosen.draw()
