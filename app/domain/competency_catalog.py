from dataclasses import dataclass


@dataclass(frozen=True)
class CompetencyCatalogEntry:
    id: str
    name: str
    description: str
    questions: tuple[str, ...]


COMPETENCY_CATALOG = (
    CompetencyCatalogEntry(
        id="self_management",
        name="Self-Management",
        description=(
            "The ability to prioritize and complete tasks "
            "in order to deliver desired outcomes within "
            "allotted time frames."
        ),
        questions=(
            "Describe a time when you independently pursued a business objective.",
            "Can you remember the last time you went about prioritising at work?",
            "When was the last time you were distracted while working on something?",
        ),
    ),

    CompetencyCatalogEntry(
        id="goal_achievement",
        name="Goal Achievement",
        description=(
            "The ability to identify and prioritize activities "
            "that lead to a goal."
        ),
        questions=(
            "Tell me of a time when you had to keep your enthusiasm levels high in the midst of a difficult situation at work.",
            "When was the last time you delivered a project within parameters of time, budget and expectations?",
            "When was the last time you set a personal goal with high standards?",
        ),
    ),

    CompetencyCatalogEntry(
        id="results_orientation",
        name="Results Orientation",
        description=(
            "The ability to identify actions necessary to "
            "complete tasks and obtain results."
        ),
        questions=(
            "Give me an example of a time when someone didn't follow-through on a commitment to you.",
            "Give me an example of a project that you have completed and the outcome.",
            "Tell me about a time when none of your supervisors were available to guide or direct you.",
            "Describe a situation in which you identified a problem and took action to correct it.",
            "Give me an example of a time when an obstacle within your control prevented you from delivering a desired result.",
        ),
    ),

    CompetencyCatalogEntry(
        id="interpersonal_skills",
        name="Interpersonal Skills",
        description=(
            "The ability to interact with others in a positive manner."
        ),
        questions=(
            "Describe the most difficult business relationship you have ever had to deal with.",
            "What is the most stressful or difficult interpersonal situation where you had to maintain your composure?",
            "Describe the most difficult, demanding person you have ever encountered.",
            "Give me an example of a situation when a personal relationship was helpful in a business situation.",
            "Describe a project where you had to deal with a diverse set of people.",
        ),
    ),

    CompetencyCatalogEntry(
        id="planning_and_organizing",
        name="Planning and Organizing",
        description=(
            "The ability to establish a process for activities "
            "that lead to the implementation of systems, "
            "procedures and outcomes."
        ),
        questions=(
            "Describe a project you had to plan for a long-term period.",
            "When was the last time you had to budget for people and finances?",
            "Tell me of a time you set a goal and it had to be re-calibrated.",
            "When was the last time you were consciously proactive in planning for something?",
        ),
    ),

    CompetencyCatalogEntry(
        id="problem_solving",
        name="Problem Solving",
        description=(
            "The ability to identify key components of a problem "
            "to formulate a solution or solutions."
        ),
        questions=(
            "Give me an example of a difficult problem you solved at work.",
            "What problem have you solved in your career that provided the greatest sense of fulfilment?",
            "Give me an example of a problem at work that you just couldn't solve.",
            "Give me an example of how you approached a complex or difficult problem.",
            "Describe a large problem you had to solve where you had to break it into smaller parts.",
        ),
    ),

    CompetencyCatalogEntry(
        id="diplomacy_and_tact",
        name="Diplomacy and Tact",
        description=(
            "The ability to treat others fairly, regardless "
            "of personal biases or beliefs."
        ),
        questions=(
            "When was the last time you lost emotional control in a difficult situation?",
            "When was the last time you applied learning to control your emotions in a difficult situation?",
            "Give me an example of a conflict with a difficult stakeholder.",
        ),
    ),

    CompetencyCatalogEntry(
        id="developing_others",
        name="Developing Others",
        description=(
            "The ability to contribute to the growth and "
            "development of others."
        ),
        questions=(
            "Give me an example of a time when you recommended a book or seminar to a subordinate.",
            "Describe how you identified and developed a training plan to improve someone's performance.",
            "Give me an example of a time you delegated a project to someone for development.",
            "Tell me about a time you worked with someone who failed to improve.",
            "Give an example of a situation where you had to hold someone accountable for poor performance.",
        ),
    ),

    CompetencyCatalogEntry(
        id="flexibility",
        name="Flexibility",
        description=(
            "The ability to readily modify, respond to and "
            "integrate change with minimal personal resistance."
        ),
        questions=(
            "Give me an example of a time when you had to make a difficult transition.",
            "Give me an example of a time when you had to suddenly change directions on an assignment.",
            "Describe a situation where you had to be flexible in handling multiple tasks.",
            "Describe a work situation where you had to accommodate someone else.",
            "Give me an instance where you had to complete a task in the presence of ambiguity.",
        ),
    ),

    CompetencyCatalogEntry(
        id="teamwork",
        name="Teamwork",
        description=(
            "The ability to cooperate with others to meet objectives."
        ),
        questions=(
            "Give me an example of a time you faced conflict while working on a team.",
            "Describe a time when you had to collaborate with a team member in another department.",
            "Tell me about a time you wish you had handled communication with a team member differently.",
            "Tell me about a time when you had to collaborate with a team member who was not responsive.",
        ),
    ),

    CompetencyCatalogEntry(
        id="decision_making",
        name="Decision Making",
        description=(
            "The ability to analyse all aspects of a situation "
            "to gain thorough insight to make decisions."
        ),
        questions=(
            "What is the most unpopular decision you ever made?",
            "Describe a decision where you put the needs of the organization before your personal preferences.",
            "Describe a situation when you had to explain the rationale for a decision.",
            "Give me an example of a decision you made quickly.",
            "Give me an example of a decision that took a very long time to make.",
            "Describe an instance where you had to consider multiple alternatives to make a decision.",
        ),
    ),

    CompetencyCatalogEntry(
        id="personal_accountability",
        name="Personal Accountability",
        description=(
            "A measure of the capacity to be answerable "
            "for personal actions."
        ),
        questions=(
            "Describe a situation when your work did not meet expectations.",
            "Tell me about a time when you had to deliver on a difficult commitment.",
            "Tell me of a situation when your role or responsibilities weren't clearly defined.",
            "Tell me about a time when you had to conform to a policy or procedure you did not agree with.",
        ),
    ),

    CompetencyCatalogEntry(
        id="resiliency",
        name="Resiliency",
        description=(
            "The ability to quickly recover from adversity."
        ),
        questions=(
            "Describe the last time you got really stressed at work.",
            "Describe a time when someone else put pressure on you.",
            "What has been your greatest failure?",
            "When was the last time you had a major setback?",
            "Tell me of a time when you had to be persistent with someone in order to reach your goal.",
        ),
    ),

    CompetencyCatalogEntry(
        id="self_starting",
        name="Self-Starting",
        description=(
            "The ability to initiate and sustain momentum "
            "without external stimulation."
        ),
        questions=(
            "Describe a project or idea that was implemented primarily because of your efforts.",
            "Describe a situation in which you recognized a potential problem as an opportunity.",
            "Tell me about a project you initiated.",
            "Tell me about a time when your initiative caused a change to occur.",
        ),
    ),

    CompetencyCatalogEntry(
        id="influencing_others",
        name="Influencing Others",
        description=(
            "The ability to personally affect others' actions, "
            "decisions, opinions or thinking."
        ),
        questions=(
            "Give me an example of a time when you listened carefully and learned something that helped you gain support.",
            "Describe a time when you needed several attempts to receive buy-in to an idea.",
            "Tell me about one of your most successful attempts to persuade others.",
            "Describe a new procedure or idea you implemented that differed considerably from the standard approach.",
            "Tell me about an instance where you had to negotiate with somebody.",
        ),
    ),

    CompetencyCatalogEntry(
        id="accountability_for_others",
        name="Accountability for Others",
        description=(
            "The ability to take responsibility for "
            "others' actions."
        ),
        questions=(
            "Tell me about a time when you had to set performance standards for a team member.",
            "Describe a time when you had to hold someone accountable.",
            "Tell me of a time when someone in your team was performing poorly.",
            "Tell me the last time you failed to correct someone.",
        ),
    ),

    CompetencyCatalogEntry(
        id="continuous_learning",
        name="Continuous Learning",
        description=(
            "The ability to take personal responsibility and "
            "action toward learning and implementing new ideas, "
            "methods, and technologies."
        ),
        questions=(
            "Tell me about the last book you read or seminar you attended.",
            "Describe how you have invested in your own professional growth in the last 12 months.",
            "Give me an example of a creative way in which you applied something you learned.",
            "Describe a task you undertook that did not succeed. What did you learn?",
            "Tell me about a time when you received negative feedback.",
        ),
    ),

    CompetencyCatalogEntry(
        id="conceptual_thinking",
        name="Conceptual Thinking",
        description=(
            "The ability to analyse hypothetical situations "
            "or abstract concepts to compile insight."
        ),
        questions=(
            "Give me an example of a project where you had to demonstrate awareness of the external business environment.",
            "Describe a time when you used financial data to identify business planning issues.",
            "Describe a time when you identified and capitalized on a market trend.",
            "Give me an example of a decision in your area that had an adverse impact on another area.",
            "Describe a project you had to plan for a long-term period.",
        ),
    ),

    CompetencyCatalogEntry(
        id="empathetic_outlook",
        name="Empathetic Outlook",
        description=(
            "The capacity to perceive and understand the "
            "feelings and attitudes of others."
        ),
        questions=(
            "Tell me about a time when you were sensitive to how another reacted in an emotional situation.",
            "Tell me about a time when you volunteered your help to someone in need.",
            "Give me an example of a time when your positive attitude motivated others.",
        ),
    ),

    CompetencyCatalogEntry(
        id="leading_others",
        name="Leading Others",
        description=(
            "The ability to organize and motivate people to "
            "accomplish goals while creating a sense of "
            "order and direction."
        ),
        questions=(
            "Think of a time when you acted as a role model for others.",
            "Tell me about a time when you were the leader of a team where you knew little and the team had the expertise.",
            "Tell me about a time you completed a goal despite resistance from others.",
            "Describe a situation when you were in charge of a project and had to enlist the help of others.",
            "Give me a situation where you think you did not succeed as a leader.",
        ),
    ),

    CompetencyCatalogEntry(
        id="conflict_management",
        name="Conflict Management",
        description=(
            "The ability to resolve different points of "
            "view constructively."
        ),
        questions=(
            "Tell me about a time you had to deal with different opinions within a team.",
            "Tell me about a time you had a disagreement with your manager or co-worker.",
            "Tell me of a time you had to mediate a conflict between colleagues.",
        ),
    ),

    CompetencyCatalogEntry(
        id="customer_focus",
        name="Customer Focus",
        description=(
            "A commitment to customer satisfaction."
        ),
        questions=(
            "Describe a time when you adjusted your workload to meet a customer's needs.",
            "Tell me about a situation where you anticipated or failed to anticipate a customer's needs.",
            "Give me an example of when you went the extra mile to meet a customer commitment.",
            "Describe a situation where you exceeded a customer's expectations.",
        ),
    ),

    CompetencyCatalogEntry(
        id="objective_listening",
        name="Objective Listening",
        description=(
            "The ability to listen to many points of view "
            "without bias."
        ),
        questions=(
            "Describe an incident when you had to listen attentively to meet a deadline.",
            "Give an example of a time when your listening skills helped meet a goal.",
            "Tell me of a time when you relied only on verbally provided information to complete a complex task.",
            "Describe a time when you realised you were distracted or biased while listening.",
        ),
    ),

    CompetencyCatalogEntry(
        id="attention_to_detail",
        name="Attention to Detail",
        description=(
            "Achieves thoroughness and accuracy when "
            "accomplishing a task through concern for "
            "all the areas involved."
        ),
        questions=(
            "Tell me about a time that you did not complete work up to normal standards.",
            "Tell me about a project that required attention to many small details.",
            "Describe a time when you had to meet a quick deadline yet deliver high-quality output.",
            "Give me an example of a routine task where vigilance on minute details was critical.",
            "Describe a task where you were required to be thorough without errors.",
        ),
    ),

    CompetencyCatalogEntry(
        id="creativity",
        name="Creativity",
        description=(
            "Discovering new opportunities and solutions for "
            "problems by looking beyond current practices "
            "and using innovative thinking."
        ),
        questions=(
            "Give me an example of a time when you challenged a conventional idea.",
            "Give me an instance where you were curious about implementing a new approach.",
            "Describe a situation where you had to brainstorm new ideas for an existing problem.",
            "Provide an instance where you challenged a senior stakeholder about a conventional practice.",
        ),
    ),
)


def get_competency(
    competency_id: str,
) -> CompetencyCatalogEntry | None:

    for competency in COMPETENCY_CATALOG:

        if competency.id == competency_id:
            return competency

    return None


def get_all_competencies() -> tuple[
    CompetencyCatalogEntry,
    ...,
]:
    return COMPETENCY_CATALOG