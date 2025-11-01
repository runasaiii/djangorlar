from datetime import datetime


def greet(name: str) -> str:
    return f"Hello, {name}!"

class Post:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self.likes = 0

        def like(self) -> None:
            self.likes += 1
        
        def summary(self) -> str:
            return f"{self.title} by {self.author}, Likes: {self.likes}"
        
        def __str__(self) -> str:
            return f"Post(title={self.title}, author={self.author}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')}, likes={self.likes})"
        

class Blog:
    def __init__(self):
        self.posts: list[Post] = []
        
    def add_post(self, post: Post) -> None:
        self.posts.append(post)

    def get_all_posts(self) -> list[Post]:
        return self.posts
            
    def find_posts_by_author(self, author: str) -> list[Post]:
        return [post for post in self.posts if post.author == author]
        
    def total_likes(self) -> int:
        return sum(post.likes for post in self.posts)
        
        
def main():
    blog = Blog()
    
    post1 = Post("My First Post", "This is the content of my first post.", "Alice")
    post2 = Post("Another Day", "Content about another day.", "Bob")
    post3 = Post("Learning Python", "Python is great for programming.", "Alice")
    
    blog.add_post(post1)
    blog.add_post(post2)
    blog.add_post(post3)
    
    post1.like()
    post1.like()
    post3.like()
    
    print("All Posts:")
    for post in blog.get_all_posts():
        print(post)
    
    print("\nPosts by Alice:")
    for post in blog.find_posts_by_author("Alice"):
        print(post)
    
    print(f"\nTotal Likes in Blog: {blog.total_likes()}")


class Comment:
    def __init__(self, post: Post, author: str, content: str):
        self.post = post
        self.author = author
        self.content = content
        self.created_at = datetime.now()
    
    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post.title} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}: {self.content}"