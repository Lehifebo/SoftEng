import logging


def read_template(path):
    # Read the contents of the template file
    with open(path, 'r') as file:
        return file.read()


class StringGenerator:
    def __init__(self, template_paths, team_list, tribe_lead_email, overview):
        # Initialize the StringGenerator object
        self.team_list = team_list
        self.template = read_template(template_paths[0])
        self.tribe_lead_template = read_template(template_paths[1])
        self.split_in_email = "\n\nsplitInEmail\n"
        self.split_between_mails = "\nsplitBetweenEmails\n"
        self.tribe_lead_email = tribe_lead_email
        self.overview = overview

    def generate_output_string(self):
        # Generate the final output string
        final_string = self.generate_teams_string()
        final_string += self.generate_overview_email()
        return final_string

    def generate_teams_string(self):
        # Generate the string for each team
        final_mail = ''

        # Exception for table mismatch
        try:
            for team in self.team_list:
                team_email = self.generate_team_email(team)
                final_mail += team_email
                final_mail += self.split_between_mails
        except KeyError:
            logging.error('You have more/less {} than columns in table')
            exit(0)
        # Remove the final splitBetweenEmails
        final_mail = final_mail.rstrip(self.split_between_mails)
        return final_mail

    def generate_team_email(self, team):
        # Generate the email string for a team
        email = ''
        email += self.add_email_list(team)
        email += self.fill_team_template(team)
        return email

    def add_email_list(self, team):
        # Generate the email list string for a team
        email_list = ''
        for item in team.emailing_list:
            email_list += item + ","
        email_list = email_list[:-1]
        email_list += self.split_in_email
        return email_list

    def fill_team_template(self, team):
        # Fill the team template with the team data
        data = [team.team_name]
        for (file, report) in team.report:
            data.append(file)
            data.append(report.to_string())
        return self.template.format(*data)

    def generate_overview_email(self):
        # Generate the overview email string

        string = ''
        string += self.split_between_mails
        string += self.tribe_lead_email
        string += self.split_in_email
        final_tables = self.filter_overview()

        # Exception for email format issues
        try:
            string += self.tribe_lead_template.format(*final_tables)
        except IndexError:
            logging.error("The number of {} is greater than 1.")
            exit(0)
        return string

    def filter_overview(self):
        # Filter and process the overview data
        final_data = []
        for (name, table) in self.overview:
            final_data.append(name)
            columns = list(table.columns)
            # Group the table and calculate the sum
            compressed_table = table.groupby('CI Config Admin Group')[columns].sum()

            # Add the 'All' row with the total sum
            compressed_table.loc['All'] = compressed_table.sum()

            # Reset the index
            compressed_table = compressed_table.reset_index()
            final_data.append(compressed_table)
        return final_data

    @staticmethod
    def create_string_file(path, string):
        # Create a file with the given path and write the string content to it
        f = open(path, "w")
        f.write(string)
        f.close()
