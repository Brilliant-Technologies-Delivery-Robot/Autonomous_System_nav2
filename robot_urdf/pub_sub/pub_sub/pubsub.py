import rclpy

from pub_sub.publisher import MinimalPublisher
from pub_sub.subscriber import MinimalSubscriber

from rclpy.executors import SingleThreadedExecutor


def main(args=None):
    rclpy.init(args=args)
    try:
        minimal_publisher = MinimalPublisher()
        minimal_subscriber = MinimalSubscriber()

        executor = SingleThreadedExecutor()
        executor.add_node(minimal_publisher)
        executor.add_node(minimal_subscriber)

        try:
            executor.spin()
        finally:
            executor.shutdown()
            minimal_publisher.destroy_node()
            minimal_subscriber.destroy_node()

    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()