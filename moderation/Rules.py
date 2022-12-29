import discord
from UI import UI

class Rules():
    def __init__(self):
            self.rule_dict = {0: ("Rule 0 - Don't be a Dick",
            "Rationale: this rule is intended to underpin our other rules. Deliberately humiliating, insulting, or otherwise upsetting other users, if we believe it to be intentional, is against what the server stands for.",
             {}, "#AC80A0" ),
            1: ("Rule 1 - No Personal Attacks",
            "Rationale: The server is intended to stand on the principle that though a person's arguements can always be criticised, a person themselves should not be.",
            {"Personal Identity":"Any assualt on a person's demographics including gender, race, sexuality, or other protected characteristics is always a violation of this rule.",
            "Heated Arguing": "When in a heated arguement, things can heated. In such a case, this rule may be made laxer. However, repeated violations of rule 1, even in arguements, can get you warnings.",
            "'You have a tendency'": "Indicating that someone habitually makes a certain error, flawed arguement, or similar is generally not in violation of this rule, unless used to humiliate, insult, or upset."
            },
            "#A48BB2"),
            2: ("Rule 2 - Making others uncomfortable",
            "Rationale: The mod team is beholden to the users to make the server a place that is comfortable, safe, and welcoming. Even if people don't directly break rules, making others directly uncomfortable is not allowed.",
            {"Reporting": "This rule relies on reports to the staff team, using either message reporting through the context menu, DM's, or other methods. ",
            "Duties": "The staff will give warnings and harsher punishments to those who are constantly reported by a range of users."
            },
            "#9B95C3"),
            3: ("Rule 3 - No NSFW content outside of #18-Plus", "Rationale: We don't want people being exposed to content that isn't age appropriate, but we do want people to have a place to discuss those elements. ",
            {"Content within 18+": "Since our vetting process cannot be guaranteed, nudity is not allowed in 18+. The channel is aimed at discussion of mature topics, rather than sexual content in itself."
            },
            "#89AAE6"),
            4: ("Rule 4- Listen to the staff",
            "Rationale: The staff aim to act to de-escalate, moderate, and improve situations on the server. As such, ignoring the staff is a good way to make the server unwelcoming for other users and fast-track your way through the warning system.",
            {}, "#6098CE"),
            5: ("Rule 5- Nicknames shouldn't be inappropriate",
            "Rationale: Your Nickname is seen multiple times by all users. By having an inflammatory nickname, you invite conflict unneccesarily.",
            {"Impersonation": "Your nickname and server profile can not be used to impersonate another user with the intent to act as them. Jokes are ok.",
            "Politically charged": "Nicknames shouldn't express an opinion on a controversial subject. If you're asked to change your nickname, change it."}, "#3685B5"),
            6: ("Rule 6 - Don't Spam", "Rationale: We want communication to be unimpeded by unneccesarily spamming, and users to be able to read without being spammed against their will.",
            {"Pings": "Random pings are always against this rule. Do not ping people for no reason. If users have their ping status set to no pings, do not ping them.",
            "Staff": "Spamming reports, suggestions, or other mod features will result in warnings.",
            "Roles": "Pinging Poll role for things that aren't polls, or mentioning roles unneccesarily is in violation of this rule."}, "#1D7BAE"),
            7: ("Rule 7 - No Slurs", "Rationale: Since we cannot guarantee what will make other users unhappy, unsafe, or uncomfortable, we forbid slurs in order to guarantee rule 2. ",
            {"Reclaimed slurs": "As above, we do not want users making slurs even about their own group. It can be unclear for us to know when this is in good faith and we know opinions aren't uniform on what is/isn't acceptable",
            "Slurs against privileged groups": "Slurs against these groups can still create conflict. As such, they're against the rules."}, "#0471A6"),
            8: ("Rule 8 - Don't Chat in Polls", "Rationale: People want to be able to rapidly parse polls, and as such excessive communication is unhelpful.", {}, "#054566")}


    def rules_embed(self, rule):
        return UI.embed(*self.rule_dict[rule])
