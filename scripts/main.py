from datetime import datetime
from graphs.graph_daily_activity import graph_daily_activity
from graphs.graph_bars_accumulated import graph_bars_accumulated
from graphs.graph_boxplot_daily import graph_boxplot_daily
from graphs.graph_histogram_sessions import graph_histogram_sessions
from graphs.graph_scatter import graph_scatter

# graph_bars_accumulated([8, 45, 61, 181], datetime(2022, 3, 27), datetime(2022, 4, 10)).show()
# graph_boxplot_daily([8, 45, 61, 181], datetime(2022, 3, 27), datetime(2022, 4, 10)).show()
graph_histogram_sessions(datetime(2022, 3, 27), datetime(2022, 4, 10)).show()
# graph_scatter(datetime(2022, 3, 27), datetime(2022, 3, 28)).show()
input()