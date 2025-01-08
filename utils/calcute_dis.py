import math

def get_closest_bin(person_coords, bins_coords):
    closest_bin = None
    min_distance = float('inf')

    for bin_coords in bins_coords:
        distance = math.sqrt((person_coords[0] - bin_coords[0])**2 + (person_coords[1] - bin_coords[1])**2)
        if distance < min_distance:
            min_distance = distance
            closest_bin = bin_coords
    return bins_coords.index(closest_bin)

if __name__ == '__main__':
    # 示例
    person = (3, 4)
    bins = [(1, 2), (5, 6), (7, 8)]
    closest = get_closest_bin(person, bins)
    print(f"The closest bin is at {closest}")
