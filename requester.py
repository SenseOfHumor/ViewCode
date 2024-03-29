import requests
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.subplots as sp
import plotly.express as px

class InvalidUsernameError(Exception):
    """Exception raised for invalid usernames or no data found for a user."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)
class LeetcodeRequester:
    
    def __init__(self):
        self.url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
        }
        self.metrics_map = {}  # Initialize metrics_map as an instance variable

    def ask(self, username):
        url = "https://leetcode.com/graphql"

        query = f'''
        {{
          matchedUser(username: "{username}") {{
            username
            submitStats: submitStatsGlobal {{
              acSubmissionNum {{
                difficulty
                count
                submissions
              }}
            }}
          }}
        }}
        '''

        headers = {
            "Content-Type": "application/json",
        }

        data = {"query": query}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise InvalidUsernameError(f"Invalid username or API request failed. Error: {err}")

        result = response.json()

        # Check if the expected structure is present in the response
        matched_user = result.get("data", {}).get("matchedUser")
        if not matched_user:
            raise InvalidUsernameError(f"Invalid username or no data found for the user: {username}")

        submit_stats = matched_user.get("submitStats", {}).get("acSubmissionNum", [])

        # Organizing the data into a dictionary
        for submission_info in submit_stats:
            difficulty = submission_info.get("difficulty")
            count = submission_info.get("count")
            submissions = submission_info.get("submissions")

            # Adding metrics to the dictionary, excluding 'All'
            #if difficulty != 'All':
            self.metrics_map[difficulty] = {"count": count, "submissions": submissions}

        print(self.metrics_map)

        return self.metrics_map

    def output(self):
        # Create a Plotly table without the 'Count' column
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Difficulty 🤯', 'Submissions 📥']),
            cells=dict(values=[
                list(self.metrics_map.keys()),
                [metrics['submissions'] for metrics in self.metrics_map.values()],
            ])
        )])

        # Update layout
        fig.update_layout(
            title='Leetcode Metrics 📈',
            # height=600,  # Adjust the height
            # width=400,   # Adjust the width)
        )
        return fig

        

    def generate_horizontal_bar_chart(self):
        # Extracting data for the chart
        difficulties = list(self.metrics_map.keys())
        counts = [metrics['count'] for metrics in self.metrics_map.values()]
        submissions = [metrics['submissions'] for metrics in self.metrics_map.values()]

        # Creating horizontal bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=difficulties,
            x=counts,
            orientation='h',
            name='Count'
        ))

        fig.add_trace(go.Bar(
            y=difficulties,
            x=submissions,
            orientation='h',
            name='Submissions'
        ))

        fig.update_layout(
            barmode='stack',
            title='Leetcode Submission Metrics',
            xaxis_title='Metrics',
            yaxis_title='Difficulty',
        )

        return fig

    def generate_pie_chart(self):
        labels = list(self.metrics_map.keys())
        values = [metrics['count'] for metrics in self.metrics_map.values()]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(title='Leetcode Submission Metrics (Count)')
        
        return fig

    def generate_donut_chart(self):
      labels = list(self.metrics_map.keys())
      values = [metrics['count'] for metrics in self.metrics_map.values()]

      fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.7)])
      fig.update_layout(
          #title='Leetcode Submission Metrics (Count)',
          height=600,  # Adjust the height
          width=600,   # Adjust the width
        #   margin=dict(l=20, r=20, t=20, b=20),  # Adjust the margins (left, right, top, bottom)
        #   paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        #   plot_bgcolor='rgba(0,0,0,0)',   # Make the plot area background transparent
        # Adjust the y-axis position
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
      )

      return fig

    

    def generate_scatter_plot(self):
        difficulties = list(self.metrics_map.keys())
        counts = [metrics['submissions'] for metrics in self.metrics_map.values()]

        # Creating scatter plot
        fig = go.Figure(data=go.Scatter(x=difficulties, y=counts, mode='markers', text=counts))

        # Update layout to make the scatter plot uninteractive
        fig.update_layout(
            #title='Leetcode Submission Metrics (Scatter Plot)',
            xaxis_title='Difficulty',
            yaxis_title='Submissions',
            # height=400,  # Adjust the height
            # width=300,   # Adjust the width
        )

        # Disable hover interactions
        fig.update_layout(hovermode=False)

        return fig






    

    # def generate_nightingale_rose_diagram(self):
    #     values = [metrics['count'] for metrics in self.metrics_map.values()]
    #     difficulties = list(self.metrics_map.keys())

    #     fig = go.Figure(data=[go.Pie(labels=difficulties, values=values, hole=0.4)])

    #     fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
    #                       marker=dict(colors=px.colors.sequential.RdBu))

    #     fig.update_layout(
    #         title_text="Leetcode Submission Metrics (Rose Chart)",
    #         annotations=[dict(text='Count', x=0.5, y=0.5, font_size=20, showarrow=False)]
    #     )

    #     return fig

           
