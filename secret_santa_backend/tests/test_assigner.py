# import pytest
# from app.assigner import SecretSantaAssigner, Employee

# def make_emps(n):
#     return [Employee(name=f"User{i}", email=f"user{i}@example.com") for i in range(n)]

# def test_basic_3():
#     emps = make_emps(3)
#     assigner = SecretSantaAssigner(emps)
#     assignments = assigner.assign()
#     assert len(assignments) == 3
#     # check nobody assigned to self
#     for g, r in assignments:
#         assert g.email != r.email

# def test_previous_constraint_blocks_simple():
#     emps = make_emps(3)
#     previous = {
#         'user0@example.com': 'user1@example.com',
#         'user1@example.com': 'user2@example.com',
#         'user2@example.com': 'user0@example.com'
#     }
#     assigner = SecretSantaAssigner(emps, previous)
#     assignments = assigner.assign()
#     assert len(assignments) == 3

# def test_no_solution():
#     # 2 employees; both exclude the other via previous -> impossible
#     e0 = Employee("A","a@x.com")
#     e1 = Employee("B","b@x.com")
#     prev = {'a@x.com':'b@x.com', 'b@x.com':'a@x.com'}
#     assigner = SecretSantaAssigner([e0,e1], prev)
#     with pytest.raises(RuntimeError):
#         assigner.assign()
