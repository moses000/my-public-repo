package balancer

type RoundRobin struct {
	targets []string
	i       int
}

func NewRoundRobin(targets []string) *RoundRobin {
	return &RoundRobin{targets: targets}
}

func (r *RoundRobin) Next() string {
	if len(r.targets) == 0 {
		return ""
	}
	t := r.targets[r.i]
	r.i = (r.i + 1) % len(r.targets)
	return t
}
