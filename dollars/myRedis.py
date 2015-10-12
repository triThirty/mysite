__author__ = 'triThirty'
import redis

def connect():
    rds=redis.StrictRedis()
    return rds
