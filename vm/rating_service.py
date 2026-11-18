class RatingService:
    def build_map(self, tasks, staff_list):
        m = {s.name: {"p": 0, "t": 0} for s in staff_list}
        for task in tasks:
            avg = task.average_score()
            if not avg:
                continue
            for name in task.performer_list():
                if name not in m:
                    continue
                if task.status == "completed":
                    m[name]["p"] += avg
                elif task.status in ("assigned", "in_progress"):
                    m[name]["t"] += avg
        return {k: {**v, "tot": v["p"] + v["t"]} for k, v in m.items()}