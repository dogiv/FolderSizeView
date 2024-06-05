import os
import matplotlib.pyplot as plt
import mplcursors

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def display_sizes(start_path):
    size_label_pairs = []

    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            item_size = int(get_size(item_path) / 1024 / 1024)  # Convert to MB
            size_label_pairs.append((item_size, item + '/'))
        elif os.path.isfile(item_path):
            item_size = int(os.path.getsize(item_path) / 1024 / 1024)
            size_label_pairs.append((item_size, item))

    # Sort by size and select the top 30
    size_label_pairs.sort(reverse=True, key=lambda x: x[0])
    size_label_pairs = size_label_pairs[:30]

    # Separate sizes and labels
    sizes, labels = zip(*size_label_pairs)

    plot_bar_graph(sizes, labels, start_path)

def on_click(event, bars, labels, start_path):
    if event.mouseevent.dblclick:
        clicked_bar = event.artist
        for i, bar in enumerate(bars):
            if bar == clicked_bar:
                clicked_item = labels[i]
                if clicked_item.endswith('/'):  # it's a folder
                    subfolder_path = os.path.join(start_path, clicked_item[:-1])
                    display_sizes(subfolder_path)
                break

def plot_bar_graph(sizes, labels, start_path):
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(range(len(labels)), sizes, color='skyblue', picker=5)
    ax.set_xlabel('Size in Megabytes')
    ax.set_ylabel('Files/Folders')
    ax.set_title(f'Size-on-disk of Files and Subfolders in {os.path.basename(start_path)}')
    ax.invert_yaxis()
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize='small')  # Set smaller font size for labels

    # Connecting the click event
    fig.canvas.mpl_connect('pick_event', lambda event: on_click(event, bars, labels, start_path))

    # Adding customized tooltips
    cursor = mplcursors.cursor(hover=True)
    @cursor.connect("add")
    def on_add(sel):
        sel.annotation.set_text(labels[sel.target.index])

    plt.show()

if __name__ == '__main__':
    args = os.sys.argv
    if len(args) > 1:
        folder_path = args[1]
    else:
        folder_path = input("Enter the path of the folder: ")
    # remove trailing slash if any
    if folder_path.endswith('/'):
        folder_path = folder_path[:-1]
    display_sizes(folder_path)
