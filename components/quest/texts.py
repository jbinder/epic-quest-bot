texts = {
    'missing-title': lambda name: f"Please include a title, {name}!",
    'quest-added': "Dadsching!! A new quest has been added!",
    'quests-open': "Open quests:",
    'quests-done': "Completed quests:",
    'select-quest-to-complete': "Select the quest you want to complete...",
    'no-quest-to-complete': "There are currently no open quests, go find some!",
    'quest-completed': lambda title: f"Whooopwhoop!! Quest '{title}' has been completed!",
    'quest-complete-error': lambda title: f"Unable to complete quest '{title}' :(",
    'stats': lambda count, done: f"From {count} quests you already completed {done}!",
}
