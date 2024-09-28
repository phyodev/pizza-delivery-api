from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from dependencies import check_access_token_validation
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)

@order_router.get('/')
async def hello(token: check_access_token_validation=Depends()):
    """
        ## A simple hello world route
        This returns Hello world
    """
    return {"message": "Hello World"}

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel,  access_token: check_access_token_validation = Depends()):
    """
        ## Placing an order
        This requires the following
        - quantity : integer
        - pizza_size: str
    """
    username = access_token.get('username')

    user = session.query(User).filter(User.username==username).first()

    new_order = Order(
        pizza_size = order.pizza_size,
        quantity = order.quantity
    )

    new_order.user = user

    session.add(new_order)

    session.commit()

    response = {
        "id": new_order.id,
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(access_token: check_access_token_validation = Depends()):
    """
        ## List all orders
        This returns all orders and this request can be used by only staff.
    """
    username = access_token.get('username')

    user = session.query(User).filter(User.username==username).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a staff!!"
            )

@order_router.get('/orders/{id}')
async def get_order_by_id(id: int, access_token: check_access_token_validation = Depends()):
    """
        ## Get specific order by id
        This requires following:
        - id : integer

        This returns information for specific order and this request for only staff.
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()
    if user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()
        return jsonable_encoder(order)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="this User not allowed to carry out this request!!"
            )

@order_router.get('/user/orders')
async def get_user_orders(access_token: check_access_token_validation = Depends()):
    """
        ## Get User Orders
        This returns the orders of authenticated user.
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()

    return jsonable_encoder(user.orders)

@order_router.get('/user/order/{id}')
async def get_specific_order(id: int, access_token: check_access_token_validation = Depends()):
    """
        ## Get Specific Order
        This requires following:
        - id : integer
        This returns the specific order by id of authenticated user.
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()
    orders = user.orders

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)
    
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order {id} doesn't have ......"
            )

@order_router.put('/order/update/{id}')
async def update_order(id: int, order: OrderModel, access_token: check_access_token_validation = Depends()):
    """
        ## Update Order
        This requires following:
        - id : integer
        - quantity : integer
        - pizza_size : str
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id==id).first()
        order_to_update.quantity = order.quantity
        order_to_update.pizza_size = order.pizza_size
        session.commit()
        session.refresh(order_to_update)
        print(f'\n\n\n{order_to_update}\n\n')
        return jsonable_encoder(order_to_update)
    else:
        orders = user.orders
        for order_to_update in orders:
            if order_to_update.id == id:
                if order_to_update.confirm == False:
                    order_to_update = session.query(Order).filter(Order.id==id).first()
                    order_to_update.quantity = order.quantity
                    order_to_update.pizza_size = order.pizza_size
                    session.commit()
                    session.refresh(order_to_update)
                    return jsonable_encoder(order_to_update)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"You can't change it now because Order {id} is already confirmed ......"
                        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Order {id} doesn't have ......"
        )

@order_router.patch('/order/update/{id}')
async def update_order_status(id: int, order: OrderStatusModel, access_token: check_access_token_validation = Depends()):
    """
        ## Update Order Status
        Note - This request can be used by only staff.
        This requires following:
        - id : integer
        - order_status : str
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id==id).first()
        if order_to_update != None:
            if order_to_update.cancel == False:
                order_router.confirm = True
                order_to_update.order_status = order.order_status
                session.commit()
                session.refresh(order_to_update)
                return jsonable_encoder(order_to_update)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order {id} doesn't have ......"
                )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="this User not allowed to carry out this request!!"
        )

@order_router.patch('/order/confirm/{id}')
async def confirm_order(id: int, access_token: check_access_token_validation = Depends()):
    """
        ## Confirm Order
        Note - This request can be used by only staff. After confirmed the orders, cusomters can't change their orders.
        This requires following:
        - id : integer
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()
    
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id==id).first()
        if order_to_update != None:
            if order_to_update.cancel == False:
                order_to_update.confirm = True
                session.commit()
                session.refresh(order_to_update)
                return f"Order {order_to_update.id} is confirmed ....  :)"
            else:
                return f"No! Order {order_to_update.id} is already cancelled. You can't confirm now ....  :("
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order {id} doesn't have ......"
                )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="this User not allowed to carry out this request!!"
        )

@order_router.patch('/order/cancel/{id}')
async def cancel_order(id: int, access_token: check_access_token_validation = Depends()):
    """
        ## Cancel Order
        This requires following:
        - id : integer
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()

    if user.is_staff == True:
        order_to_update = session.query(Order).filter(Order.id==id).first()
    else:
        orders = user.orders
        order_to_update = None
        for order in orders:
            if order.id == id:
                order_to_update = order
    if order_to_update != None:
        if order_to_update.confirm == False:
            order_to_update.cancel = True
            session.commit()
            session.refresh(order_to_update)
            return f"Order {order_to_update.id} is cancelled ....  :)"
        else:
            return f"No! Order {order_to_update.id} is already confirmed. You can't cancel now ....  :("
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order {id} doesn't have ......"
            )
    
@order_router.delete('/order/delete/{id}')
async def delete_order(id: int, access_token: check_access_token_validation = Depends()):
    """
        ## Delete Order
        This requires following:
        - id : integer
    """
    username = access_token.get('username')
    user = session.query(User).filter(User.username==username).first()

    if user.is_staff == True:
        order_to_delete = session.query(Order).filter(Order.id==id).first()
    else:
        orders = user.orders
        order_to_delete = None
        for order in orders:
            if order.id == id:
                order_to_delete = order
    if order_to_delete != None:
        order_id = order_to_delete.id
        if (order_to_delete.confirm == False and order_to_delete.cancel == False) or (order_to_delete.confirm == False and order_to_delete.cancel == True) or order_to_delete.order_status == 'DELIVERED':
            session.delete(order_to_delete)
            session.commit()
            return f"Order {order_id} is deleted ....  :)"
        else:
            return f"No! Order {order_id} is already confirmed. You can't delete now ....  :("
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order {id} doesn't have ......"
            )