import tkinter as TK
import main
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime as dt

btn1pressed = False

is_right = True

lst_of_pairs = []

eid = ""
right_line = True

canvas_width = 800
canvas_height = 600
dst = canvas_width / 32


def mouse1press(event):
    global btn1pressed
    print(event.x, event.y)
    pair = []
    pair.append(event.x)
    pair.append(event.y)
    lst_of_pairs.append(pair)
    btn1pressed = True
    if btn1pressed == True:
        global xorig, yorig
        if event.x > lst_of_pairs[len(lst_of_pairs) - 2][0]:
            the_canvas.create_line(xorig, yorig, event.x, event.y,
                                   smooth=TK.TRUE, fill="yellow", width=5, tag="new_line")
        else:
            if len(lst_of_pairs) >= 2:
                lst_of_pairs.pop(-1)
        xorig = lst_of_pairs[len(lst_of_pairs) - 1][0]
        yorig = lst_of_pairs[len(lst_of_pairs) - 1][1]


def draw_grid():
    for i in range(0, 32):
        the_canvas.create_line(i * dst, 0, i * dst, canvas_height, fill="yellow", width=2)
    the_canvas.create_line(0, canvas_height, canvas_width, canvas_height, fill="blue", width=5)
    the_canvas.create_line(canvas_width - 20, canvas_height - 20, canvas_width, canvas_height, fill="blue", width=5)
    the_canvas.create_line(3, 0, 3, canvas_height + 5, fill="blue", width=5)
    the_canvas.create_line(0, 0, 20, 20, fill="blue", width=5)


def draw_highlighted_column(nr):
    the_canvas.create_rectangle(nr * dst + dst / 2, 0, dst, canvas_height, fill="green")


def draw_normal_column(nr):
    the_canvas.create_rectangle(nr * dst + dst / 2, 0, dst, canvas_height, fill="black")


def create_lst(nr_of_columns):
    lst = []
    for i in range(0, nr_of_columns):
        lst.append(i * dst)
    return lst


def approximate_to_column(nr):
    lst = create_lst(32)
    ret = 0
    mini = 100040239
    for i in range(0, len(lst)):
        var = int(lst[i] - nr)
        var = abs(var)
        if var < mini:
            ret = i
            mini = var
    return lst[ret]


def calculate_each_draw(event):
    x = event.x
    y = event.y
    pair = []
    x = approximate_to_column(x)
    pair.append(int(x))
    pair.append(y)
    global xorig, yorig
    if len(lst_of_pairs) == 0:
        perc = 100 - ((true_y[0]-min(true_y))*100)/(max(true_y)-min(true_y))
        value = perc*canvas_height/100
        lst_of_pairs.append([0, value])
        xorig = lst_of_pairs[len(lst_of_pairs) - 1][0]
        yorig = lst_of_pairs[len(lst_of_pairs) - 1][1]
    lst_of_pairs.append(pair)
    if event.x > lst_of_pairs[len(lst_of_pairs) - 2][0]:
        the_canvas.create_line(xorig, yorig, x, y, smooth=TK.TRUE, fill="yellow", width=5, tag="new_line")
    else:
        if len(lst_of_pairs) >= 2:
            lst_of_pairs.pop(-1)
    xorig = lst_of_pairs[len(lst_of_pairs) - 1][0]
    yorig = lst_of_pairs[len(lst_of_pairs) - 1][1]


def check_valid__(event):
    x = event.x
    temp_x = int(approximate_to_column(x))
    if temp_x == (i - 1) * dst:
        calculate_each_draw(event)
        repaint(event)
    if i == 33:
        give_stuff_____________()


def repaint(event):
    global i
    draw_highlighted_column(i)
    if i >= 1:
        for j in range(0, i):
            draw_normal_column(j)
    if i == 1:
        draw_highlighted_column(i - 1)
    draw_grid()
    redraw_graph(lst_of_pairs)
    draw_legend()
    i = i + 1


def draw_legend():
    interval_x = canvas_width / 8
    interval_y = canvas_height / 8
    diff = (max(true_y) - min(true_y))/8
    font_size = 12
    color = "white"
    for i in range(0, 8):
        the_canvas.create_text(i * interval_x + 50, canvas_height - 15, text=y_draw[(i * 4) + 2], fill=color, angle=30, font=("Purisa", font_size))
        the_canvas.create_text(28, (i+1) * interval_y-60, text=str(round(min(true_y)+(8-i)*diff, 2)), fill=color, font=("Purisa", font_size))


def redraw_graph(lst):
    for i in range(0, len(lst) - 1):
        the_canvas.create_line(lst[i][0], lst[i][1], lst[i + 1][0], lst[i + 1][1], fill="yellow", width=5)


def give_stuff_____________():
    # print("S-o gatat!")
    plt.close('all')
    root.destroy()
    pred_y = []
    for i in range(0, len(lst_of_pairs)):
        y_perc = 100 - ((lst_of_pairs[i][1]*100)/canvas_height)
        y_val = (y_perc*(max(true_y)-min(true_y)))/100 + min(true_y)
        pred_y.append(y_val)
    # print(pred_y)
    diffs = main.get_diffs(dates_draw, true_y, pred_y)
    slopes = main.get_slopes(dates_draw, true_y, pred_y)
    pred_volat = main.get_lst_volat(pred_y)
    true_volat = main.get_lst_volat(true_y)

    print("------------------------------------------------")
    print("RESULTS OF PREDICTION ATTEMPT OF " + val)
    print("------------------------------------------------")
    print("Average difference: " + str(diffs["avg"]) + '%')
    print("Minimum difference: " + str(diffs["min"]) + '%')
    print("Maximum difference: " + str(diffs["max"]) + '%')
    print()
    print("Average slope change: " + str(slopes["avg_change_%"]) + '%')

    print("Number of correct slopes: " + str(slopes["correct_slopes"]) + "/" + str(slopes["total_slopes"]))
    print()
    print(val + " true volatility: " + str(true_volat) + "%")
    print(val + " predicted volatility " + str(pred_volat) + '%')
    print()
    print("------------------------------------------------")
    print("Details:")
    print("------------------------------------------------")
    print()
    print("List of difference between predicted values and actual values:")
    for i in range(0, len(dates_draw)):
        print(str(i) + ". " + str(dates_draw[i]) + ' - ' +  str(diffs["vals"][i]))

    print()
    print("List of Slope changes between predicted values and actual values: ")
    for i in range(0, len(slopes["slope_change"])):
        print(str(i) + ". " + str(dates_draw[i]) + ' - ' + str(slopes["slope_change"][i]))
    print()
    print("------------------------------------------------")
    print("Prediction concluded.")

    fig_draw, ax_draw = plt.subplots(1)
    ax_draw.plot(dates_draw, pred_y, "b-", dates_draw, true_y, "r-")
    pred_patch = mpatches.Patch(color='blue', label='Prediction')
    true_patch = mpatches.Patch(color='red', label='Actual data')
    ax_draw.set_ylim([min(true_y), max(true_y)])
    ax_draw.legend(handles=[pred_patch, true_patch])
    ax_draw.set_title(val + "/USD Prediction")
    fig_draw.autofmt_xdate()
    plt.show()


# __________________-MAIN-__________________________#

symbols = ["BTC", "ETH", "BCH", "BTG", "DASH", "XRP", "ZEC"]
correct_input = False
while correct_input is False:
    print("Please input the symbol of a coin from cex.io which you want to predict:")
    val = input("--->")

    for symbol in symbols:
        if val == symbol:
            correct_input = True

    if correct_input is False:
        print("There is no such symbol on cex.io. Please try again.")
    else:
        print("Your input was: " + val + ". Continue?(Y/N)")
        val2 = input("--->")
        if val2 is "Y":
            print("Loading...")
        else:
            print("Restarting...")
            correct_input = False
graph = main.get_coin_prices_dates(val)
x = []
y = []
x_draw = []
y_draw = []
dates_draw = []
dates = []
min_val = 100000000
max_val = 0
true_y = []

for i in range(0, len(graph[0])):
    x.append(graph[0][i][0])
    dates.append(dt.datetime.fromtimestamp(graph[0][i][0]))
    y.append(graph[0][i][1])
    if y[-1] >= max_val:
        max_val = y[-1]
    if y[-1] <= min_val:
        min_val = y[-1]

    x_draw.append(graph[1][i][0])
    var = dt.datetime.fromtimestamp(graph[1][i][0]).strftime("%H-%M")
    dates_draw.append(dt.datetime.fromtimestamp(graph[1][i][0]))
    y_draw.append(var)
    true_y.append(graph[1][i][1])


# __________________-DRAW-______________________________#


root = TK.Tk()
root.title("Canvas")
root.minsize(canvas_width + 25, canvas_height + 15)

i = 1

size = str(canvas_width) + 'x' + str(canvas_height)

root.geometry('800x600')
the_canvas = TK.Canvas(root, width=canvas_width, height=canvas_height, background="black")

draw_grid()
the_canvas.create_text(250, 250, text="Can you predict the cryptos?!", fill="white", angle=45)

the_canvas.pack()
# the_canvas.bind("<Motion>", mousemove)
the_canvas.bind("<ButtonPress-1>", check_valid__)
# the_canvas.bind("<ButtonRelease-1>", repaint)

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(dates, y, "b-")
ax.set_title(val + "/USD")
fig.autofmt_xdate()
plt.show()

root.mainloop()
