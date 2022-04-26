FROM nginx:latest

ARG work_dir=/etc/nginx

ADD conf/nginx.conf $work_dir
ADD conf/mime.types $work_dir
ADD conf/default.conf $work_dir/conf.d/
ADD conf/proxy_params $work_dir/proxy_params
