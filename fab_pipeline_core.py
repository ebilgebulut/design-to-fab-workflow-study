import math

#Artificial Wall Library
walls = [
    {"id": "W1", "length_mm": 4200, "height_mm": 2700, "has_framing_type": True},
    {"id": "W2", "length_mm": 3000, "height_mm": 2700, "has_framing_type": False},
    {"id": "W3", "length_mm": 5400, "height_mm": 2700, "has_framing_type": True},
]

#QA/QC- BIM Data Check Functions
def check_wall(wall):
    if not wall["has_framing_type"]:
        return False, "Framing type missing"
    elif wall["length_mm"] <= 0:
        return False, "the length value should be bigger than 0"
    elif wall["height_mm"] <= 0:
        return False, "the height value should be bigger than 0"
    return True, "Ok"

passed_walls = []

#Testing Walls using QA Function, eliminating the passed ones for test in the next steps
for wall in walls:
    passed, message = check_wall(wall)
    print(f"{wall['id']}: passed={passed}, message={message}")
    if passed:
        passed_walls.append(wall)

print(passed_walls)

#Rule sets as a dict/json format that represents the differen manufacturer data, limits, parameters etc
RULE_A = {"name": "Standard", "stud_spacing_mm": 400, "panel_width_mm": 1200}
RULE_B = {"name": "Wide spacing", "stud_spacing_mm": 600, "panel_width_mm": 2400}

#creating a function to make some fab calculations/data checks with using wall data and the manufacturer input 
def calculate_wall_fab(wall, rule):
    stud_count = math.ceil(wall["length_mm"] / rule["stud_spacing_mm"]) + 1
    panel_count = math.ceil(wall["length_mm"] / rule["panel_width_mm"])
    return {"wall_id": wall["id"], "stud_count": stud_count, "panel_count": panel_count}

rejected_count = len(walls) - len(passed_walls)
print(f"Rejected walls: {rejected_count}")

#applying the fab calculation function to the selected/passed element library set(walls) and report
rules = [RULE_A, RULE_B]
for rule in rules:
    total_studs = 0
    total_panels = 0
    for wall in passed_walls:
        result = calculate_wall_fab(wall, rule)
        total_studs += result["stud_count"]
        total_panels += result["panel_count"]
    print(f"{rule['name']}: total studs={total_studs}, total panels={total_panels}")
