
import numpy as np
import pandas as pd


class GameGenerator:
    def __init__(self, combined_data, df):
        self.combined_data = combined_data
        self.df = df
        self.transition_matrix = self.generate_transition_matrix()

    def generate_transition_matrix(self):
        """
        Generate a transition matrix from the DataFrame.

        :param df: DataFrame with the game data.
        :return: Transition matrix as a DataFrame.
        """

        # Create a shifted version of the label column to represent the next action
        self.df['next_label'] = self.df['label'].shift(-1)

        # Filter out rows where the next action belongs to a different match
        self.df['next_match'] = self.df['match_id'].shift(-1)
        self.df.loc[self.df['match_id'] != self.df['next_match'], 'next_label'] = None

        # Creating a pivot table to get the counts of each transition
        transition_counts = self.df.groupby(['label', 'next_label']).size().unstack(fill_value=0)
        
        # Convert counts to probabilities by dividing by the row sum
        transition_matrix = transition_counts.div(transition_counts.sum(axis=1), axis=0)
        
        return transition_matrix

    def assign_norm(self, action):
        """
        Assigns stochastic norms to an action based on the analyzed statistics of norms in the dataset.

        :param action: str, the action for which norms are to be assigned
        :return: list, a list of norms assigned to the given action
        """

        # Extracting norms and labels for analysis
        norms_data = [{'label': entry['label'], 'norm': entry['norm']} for entry in self.combined_data]
        
        # Converting to DataFrame for easier analysis       
        norms_df = pd.DataFrame(norms_data)

        # Calculate the average and standard deviation of norms for each action and the average length of norm lists
        norms_analysis = norms_df.copy()
        norms_analysis['avg_norm'] = norms_analysis['norm'].apply(lambda x: sum(x) / len(x) if x else 0)
        norms_analysis['std_norm'] = norms_analysis['norm'].apply(lambda x: np.std(x) if x else 0)
        norms_analysis['len_norm'] = norms_analysis['norm'].apply(len)
        
        # Group by label to get the averages and standard deviations for each action
        norms_stats = norms_analysis.groupby('label').agg({
            'avg_norm': 'mean',
            'std_norm': 'mean',
            'len_norm': 'mean'
        }).reset_index()

        # Extracting statistics for the action
        action_stats = norms_stats[norms_stats['label'] == action]
        avg_norm = action_stats['avg_norm'].values[0]
        std_norm = action_stats['std_norm'].values[0]
        avg_len = int(action_stats['len_norm'].values[0])
        
        # The mean and standard deviation of the log-normal distribution are not the same as the mean and standard deviation
        # of the generated values. We use the following formulas to find the parameters of the distribution.
        mu = np.log(avg_norm / np.sqrt(1 + (std_norm / avg_norm) ** 2))
        sigma = np.sqrt(np.log(1 + (std_norm / avg_norm) ** 2))
        
        # Sampling norms from a log-normal distribution
        norm = np.random.lognormal(mean=mu, sigma=sigma, size=avg_len)
        
        return norm.tolist()

    def assign_gait_length(self, action):
        """
        Assigns stochastic gait lengths to an action based on the gait lengths in the original dataset.

        :param action: str, the action for which gait length is to be assigned
        :return: float, a gait length assigned to the given action
        """

        # Extracting gait lengths and labels for analysis
        gait_lengths_data = [{'label': entry['label'], 'gait_length': len(entry['norm']) / 50} for entry in self.combined_data]
        
        # Converting to DataFrame for easier analysis
        gait_lengths_df = pd.DataFrame(gait_lengths_data)
        
        # Calculate the average and standard deviation of gait lengths for each action
        gait_lengths_stats = gait_lengths_df.groupby('label').agg({
            'gait_length': ['mean', 'std']
        }).reset_index()

        # Extracting statistics for the action
        action_stats = gait_lengths_stats[gait_lengths_stats['label'] == action]
        avg_gait_length = action_stats[('gait_length', 'mean')].values[0]
        std_gait_length = action_stats[('gait_length', 'std')].values[0]
        
        # Sampling gait length from a normal distribution
        gait_length = np.abs(np.random.normal(loc=avg_gait_length, scale=std_gait_length))
        
        # Ensure gait length is within bounds, resample if not
        while gait_length < 0.1 or gait_length > 3:
            gait_length = np.abs(np.random.normal(loc=avg_gait_length, scale=std_gait_length))
        return gait_length

    def generate_game(self, start_action, desired_duration_minutes, game_style):
        """
        Generate a simulated game sequence based on a Markov Chain model.
        
        :param start_action: str, initial action to start the game sequence
        :param desired_duration_minutes: int, desired total duration for the game sequence in minutes
        :param game_style: str, chosen game style affecting the transition probabilities ('attacking', 'defensive', or 'neutral')
        :return: list, a nested list of dictionaries where each dictionary represents an action with its associated norm 
        """
        
        game_sequence = [{'label': start_action, 'norm': self.assign_norm(start_action)}]
        total_gait_length = self.assign_gait_length(start_action)
        
        # A dictionary to hold the game style and corresponding adjustments to probabilities
        adjustment_factors = {
            'attacking': {'shot': 2, 'pass': 2, 'dribble': 1.5, 'cross': 2},
            'defensive': {'tackle': 2, 'run': 2, 'pass': 0.5, 'dribble': 0.5}
        }

        while total_gait_length < desired_duration_minutes * 60:
            current_action = game_sequence[-1]['label']
            next_action_choices = list(self.transition_matrix.columns)
            next_action_probabilities = self.transition_matrix.loc[current_action].values.copy()
            
            # Adjust game style probabilities
            if game_style in adjustment_factors:
                for action, adjustment in adjustment_factors[game_style].items():
                    next_action_probabilities[next_action_choices.index(action)] *= adjustment
           
            # Normalize the probabilities
            next_action_probabilities /= sum(next_action_probabilities)
            next_action = np.random.choice(next_action_choices, p=next_action_probabilities)
            
            # Check for constraints and adjust next action if necessary
            if len(game_sequence) >= 2 and game_sequence[-2]['label'] == next_action == 'shot':
                next_action = np.random.choice([action for action in next_action_choices if action != 'shot'])
            elif len(game_sequence) >= 2 and game_sequence[-2]['label'] == next_action == 'cross':
                next_action = np.random.choice([action for action in next_action_choices if action != 'cross'])
            
            norm_values = self.assign_norm(next_action)
            gait_length = self.assign_gait_length(next_action)
            game_sequence.append({'label': next_action, 'norm': norm_values})
            
            # Update total_gait_length with the gait length for the chosen action
            total_gait_length += gait_length
            
        return game_sequence
