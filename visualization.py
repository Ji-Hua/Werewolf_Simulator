import streamlit as st
import numpy as np
import copy

st.title('烂柯游艺社狼人杀胜率模拟器')

# hyper-parameters
wolf_label = 'wolf'
villager_label = 'villager'
god_label = 'god'
badge = False
# badge_inheritable = False
p_follow = 0.9
# wolf vote
wolf_arrangement = False



game_setting = {}
num_wolves = st.sidebar.number_input('狼人数量', value=4,
    min_value=1, max_value=12, step=1)
num_gods = st.sidebar.number_input('神位数量', value=4,
    min_value=1, max_value=12, step=1)
num_villagers = st.sidebar.number_input('平民数量', value=4,
    min_value=1, max_value=12, step=1)
num_players = num_wolves + num_gods + num_villagers

# parameters in side bar
st.markdown(f'{num_players}人局  狼人: {num_wolves}  神民: {num_gods}  平民: {num_villagers}')
st.markdown('无警徽 狼人无格式 白板神 屠边胜利')
st.markdown('---')

# wolf_levels_dict = {'新手': 0.5, '普通': 0.7, '专家': 0.9}
wolf_level = st.sidebar.number_input('狼人找到神的概率为',
    min_value=0.0, max_value=1.0, step=0.01)
st.sidebar.markdown('注：0.0 表示狼人随机选择目标')
game_setting['wolf'] = wolf_level

# how likely a player is able to distinguish wolf if he is not wolf
# random guess would be 4/11, 36.3%
# villager_levels_dict = {'新手': 0.45, '普通': 0.7, '专家': 0.95}
villager_level = st.sidebar.number_input('好人找到狼人的概率为', value=0.50,
    min_value=0.0, max_value=1.0, step=0.01)
game_setting['villager'] = villager_level
st.sidebar.markdown('---')

num_simulation = st.sidebar.number_input('进行模拟的轮数', min_value=5, max_value=100, step=5)
num_iteration = st.sidebar.number_input('每轮进行模拟的游戏数', min_value=1000, max_value=10000, step=1000)


def random_select(iterable):
    return np.random.choice(list(iterable))

def hunt(p_god, gods, villagers):
    if p_god == 0:
        n_gods = len(gods)
        n_villagers = len(villagers)
        target = random_select(list(range(1, n_gods + n_villagers + 1)))
        if target > n_gods:
            return random_select(villagers), villager_label
        else:
            return random_select(gods), god_label
    else:
        is_god = np.random.binomial(1, p_god, 1)
        if is_god:
            return random_select(gods), god_label
        else:
            return random_select(villagers), villager_label

def check_game_end(group_dict):
    if len(group_dict[god_label]) == 0:
        winner = wolf_label
    elif len(group_dict[villager_label]) == 0:
        winner = wolf_label
    elif len(group_dict[wolf_label]) == 0:
        winner = villager_label
    else:
        winner = None
    return winner

def vote(group_dict, p_wolf, wolf_arragement=False, sheriff_arrangement=None, sheriff=None, p_follow=0.9):
    good_people = group_dict[god_label].union(group_dict[villager_label])
    wolves = group_dict[wolf_label]
    all_players = good_people.union(wolves)
    vote_result = {}
    for p in good_people:
        vote_result[p] = 0
    for p in wolves:
        vote_result[p] = 0
    # wolf vote
    if sheriff and sheriff in wolves:
        vote_target = sheriff_arrangement
        vote_result[vote_target] += len(wolves)
    elif wolf_arragement:
        vote_target = random_select(good_people)
        vote_result[vote_target] += len(wolves)
    else:
        # we allow that wolf vote to another wolf
        # and wolf won't follow sheriff's arrangement unless he is a wolf
        for w in wolves:
            vote_target = random_select(all_players - set([w]))
            vote_result[vote_target] += 1
    # good people vote
    if sheriff_arrangement:
        is_follow = np.random.binomial(1, p_follow, 1)
        if is_follow:
            vote_target = sheriff_arrangement
            vote_result[vote_target] += 1
        else:
            is_wolf = np.random.binomial(1, p_wolf, 1)
            if is_wolf:
                vote_target = random_select(wolves)
                vote_result[vote_target] += 1
            else:
                vote_target = random_select(good_people - set([p]))
                vote_result[vote_target] += 1
    else:
        for p in good_people:
            is_wolf = np.random.binomial(1, p_wolf, 1)
            if is_wolf:
                vote_target = random_select(wolves)
                vote_result[vote_target] += 1
            else:
                vote_target = random_select(good_people - set([p]))
                vote_result[vote_target] += 1
    
    maxium_vote = max(vote_result.values())
    result = random_select([k for k, v in vote_result.items() if v == maxium_vote])
    if result in wolves:
        label = wolf_label
    elif result in group_dict[god_label]:
        label = god_label
    else:
        label = villager_label
    return result, label

def select_sheriff(group_dict, only_good=False):
    good_people = group_dict[god_label].union(group_dict[villager_label])
    wolves = group_dict[wolf_label]
    if only_good:
        all_candidates = good_people
    else:
        all_candidates = good_people.union(wolves)
    return random_select(all_candidates)

def sheriff_arrangement(sheriff, group_dict, p_wolf):
    good_people = group_dict[god_label].union(group_dict[villager_label])
    wolves = group_dict[wolf_label]
    # all_players = good_people.union(wolves)
    if sheriff in good_people:
        is_wolf = np.random.binomial(1, p_wolf, 1)
        if is_wolf:
            vote_target = random_select(wolves)
        else:
            vote_target = random_select(good_people - set([sheriff]))
        return vote_target
    elif sheriff in wolves:
        vote_target = random_select(good_people)
        return vote_target
    else:
        return None

def prettify_results(results):
    pretty_results = []
    grand_total = 0
    grand_wolf_victory = 0
    for r in results:
        total = r['wolf'] + r['villager']
        grand_total += total
        grand_wolf_victory += r['wolf']
        pretty_result = f"{r['wolf']}局狼人胜，狼人胜率为{float(r['wolf']/total)}, {r['villager']}局好人胜，好人胜率为{float(r['villager']/total)}"
        pretty_results.append(pretty_result)
    average_wolf_win_rate = float(grand_wolf_victory/grand_total)
    average_villager_win_rate = 1.0 - average_wolf_win_rate
    return (pretty_results, (average_wolf_win_rate, average_villager_win_rate))

# simulation
if st.sidebar.button('开始模拟'):
    overall_results = []
    st.markdown(f'好人等级为 **{villager_level}**')
    if wolf_level == 0:
        msg = f'狼人**随机**刀杀好人'
    else:
        msg = f'狼人等级为 **{wolf_level}**'
    st.markdown(msg)
    st.markdown('---')
    progress_bar = st.progress(0)
    percent = 1.0 / float(num_simulation)
    with st.spinner('模拟中...'):
        for num in range(num_simulation):
            winning_record = {
                villager_label: 0,
                wolf_label: 0
            }
            for i in range(num_iteration):
                players = list(range(1, num_players + 1))
                shuffled_players = copy.deepcopy(players)
                np.random.shuffle(shuffled_players)
                wolves = set(shuffled_players[0:num_wolves])
                gods = set(shuffled_players[num_wolves:(num_wolves+num_gods)])
                villagers = set(shuffled_players[(num_wolves+num_gods):])
                group_dict = {
                    wolf_label: wolves,
                    god_label: gods,
                    villager_label: villagers
                }
                identity_dict = {}
                for p in players:
                    if p in wolves:
                        identity_dict[p] = 'wolf'
                    elif p in gods:
                        identity_dict[p] = 'god'
                    else:
                        identity_dict[p] = 'villager'
                # game loop
                if badge:
                    sheriff = None
                while True:
                    # start hunting
                    p_god = game_setting['wolf']
                    target, label = hunt(p_god, group_dict[god_label], group_dict[villager_label])
                    group_dict[label].discard(target)
                    winner = check_game_end(group_dict)
                    if winner:
                        winning_record[winner] += 1
                        break
                    if badge:
                        if not sheriff:
                            sheriff = select_sheriff(group_dict, True)
                        sheriff_vote = sheriff_arrangement(sheriff, group_dict, game_setting['villager'])
                    else:
                        sheriff = None
                        sheriff_vote = None
                    target, label = vote(group_dict, game_setting['villager'], wolf_arrangement, sheriff_vote, sheriff, p_follow)
                    group_dict[label].discard(target)
                    winner = check_game_end(group_dict)
                    if winner:
                        winning_record[winner] += 1
                        break
            overall_results.append(winning_record)
            progress_bar.progress(percent * (num + 1))

    progress_bar.empty()
    st.markdown('**模拟结果**')
    pretty_results, averages = prettify_results(overall_results)
    st.write(f"狼人平均胜率为{averages[0]}， 好人平均胜率为{averages[1]}")
    st.write('**每轮模拟结果如下**')
    for i, pr in enumerate(pretty_results):
        st.markdown(f'**第{i+1}轮**: {pr}')