import argparse
import template

parser = argparse.ArgumentParser(
    description="Training framework for image super-resolution"
)

parser.add_argument("--debug", action="store_true", help="Enables debug mode")
parser.add_argument(
    "--template", default=".", help="You can set various templates in option.py"
)

# Hardware specifications
parser.add_argument(
    "--n_threads", type=int, default=4, help="number of threads for data loading"
)
parser.add_argument("--no_cuda", action="store_true", help="enables CUDA training")
parser.add_argument("--n_GPUs", type=int, default=1, help="number of GPUs")
parser.add_argument("--seed", type=int, default=1, help="random seed")

# Option for license plate super-resolution
parser.add_argument(
    "--std-lr-width",
    type=int,
    default=23,
    help="Standard license plate width (default 23)",
)
parser.add_argument(
    "--std-lr-height",
    type=int,
    default=16,
    help="Standard license plate height (default 16)",
)
parser.add_argument(
    "--gauss-std",
    type=float,
    default=1.6,
    help="Standard deviation for Gaussian blur (default 1.6)",
)
parser.add_argument(
    "--datatype",
    type=str,
    default="realreal",
    help="data type for license plate super-resolution:"
    + " realreal, realsimu, simureal, simusimu, all.",
)
parser.add_argument(
    "--dir-testlpt", type=str, default="./test", help="testset directory"
)
parser.add_argument("--image", type=str, default="", help="image to be super resolve")

# Data specifications
parser.add_argument(
    "--interp",
    type=str,
    default="bicubic",
    help="Interpolation to use for re-sizing"
    + " (‘nearest’, ‘lanczos’, ‘bilinear’, ‘bicubic’)",
)
parser.add_argument("--freesize", action="store_true", help="Use with ERDN")
parser.add_argument(
    "--dir_data", type=str, default="./dataset", help="dataset directory"
)
parser.add_argument(
    "--data_train", type=str, default="DIV2K", help="train dataset name"
)
parser.add_argument("--data_test", type=str, default="DIV2K", help="test dataset name")
parser.add_argument(
    "--n_train",
    type=int,
    default=800,  # I use id text file instead: id_train.txt
    help="number of training set",
)
parser.add_argument("--n_val", type=int, default=10, help="number of validation set")
parser.add_argument(
    "--offset_val",
    type=int,
    default=800,  # I use id text file instead: id_validate.txt
    help="validation index offest",
)
parser.add_argument("--ext", type=str, default="img", help="dataset file extension")
parser.add_argument("--scale", default="4", help="super resolution scale")
parser.add_argument(
    "--patch_size",
    type=int,
    default=15,  # 15 is the height of LR image
    help="output patch size",
)
parser.add_argument("--rgb_range", type=int, default=255, help="maximum value of RGB")
parser.add_argument(
    "--n_colors", type=int, default=3, help="number of color channels to use"
)
parser.add_argument("--noise", type=str, default=".", help="Gaussian noise std.")
parser.add_argument(
    "--chop_forward", action="store_true", help="enable memory-efficient forward"
)

# Model specifications
parser.add_argument("--model", default="EDSR", help="model name")

parser.add_argument("--act", type=str, default="relu", help="activation function")
parser.add_argument(
    "--pre_train", type=str, default=".", help="pre-trained model directory"
)
parser.add_argument(
    "--extend", type=str, default=".", help="pre-trained model directory"
)
parser.add_argument(
    "--n_resblocks", type=int, default=16, help="number of residual blocks"
)
parser.add_argument("--n_feats", type=int, default=64, help="number of feature maps")
parser.add_argument("--res_scale", type=float, default=1, help="residual scaling")
parser.add_argument(
    "--shift_mean", default=True, help="subtract pixel mean from the input"
)
parser.add_argument("--dilation", action="store_true", help="use dilated convolution")
parser.add_argument(
    "--precision",
    type=str,
    default="single",
    choices=("single", "half"),
    help="FP precision for test (single | half)",
)

# Option for Residual dense network (RDN)
parser.add_argument(
    "--G0", type=int, default=64, help="default number of filters. (Use in RDN)"
)
parser.add_argument(
    "--RDNkSize", type=int, default=3, help="default kernel size. (Use in RDN)"
)
parser.add_argument(
    "--RDNconfig", type=str, default="B", help="parameters config of RDN. (Use in RDN)"
)

# Option for Residual channel attention network (RCAN)
parser.add_argument(
    "--n_resgroups", type=int, default=10, help="number of residual groups"
)

parser.add_argument(
    "--reduction", type=int, default=16, help="number of feature maps reduction"
)

# Option for ERN4LSR
parser.add_argument(
    "--n_convs", type=int, default=64, help="number of core's convolution layers"
)

# Training specifications
parser.add_argument("--reset", action="store_true", help="reset the training")
parser.add_argument(
    "--test_every", type=int, default=100, help="do test per every N batches"
)
parser.add_argument("--epochs", type=int, default=300, help="number of epochs to train")
parser.add_argument(
    "--resume", type=int, default=-1, help="load the model from the specified epoch"
)
parser.add_argument(
    "--batch_size", type=int, default=8, help="input batch size for training"
)
parser.add_argument(
    "--split_batch", type=int, default=1, help="split the batch into smaller chunks"
)
parser.add_argument(
    "--self_ensemble", action="store_true", help="use self-ensemble method for test"
)
parser.add_argument(
    "--test_only", action="store_true", help="set this option to test the model"
)

# Optimization specifications
parser.add_argument("--lr", type=float, default=1e-4, help="learning rate")
parser.add_argument(
    "--lr_decay", type=int, default=150, help="learning rate decay per N epochs"
)
parser.add_argument(
    "--decay_type", type=str, default="step", help="learning rate decay type"
)
parser.add_argument(
    "--gamma", type=int, default=0.5, help="learning rate decay factor for step decay"
)
parser.add_argument(
    "--optimizer",
    default="ADAM",
    choices=("SGD", "ADAM", "RMSprop"),
    help="optimizer to use (SGD | ADAM | RMSprop)",
)
parser.add_argument("--momentum", type=float, default=0.9, help="SGD momentum")
parser.add_argument("--beta1", type=float, default=0.9, help="ADAM beta1")
parser.add_argument("--beta2", type=float, default=0.999, help="ADAM beta2")
parser.add_argument(
    "--epsilon", type=float, default=1e-8, help="ADAM epsilon for numerical stability"
)

# Loss specifications
parser.add_argument(
    "--loss", type=str, default="1*L1", help="loss function configuration"
)
parser.add_argument(
    "--skip_threshold",
    type=float,
    default="100",
    help="skipping batch that has large error",
)

# Log specifications
parser.add_argument("--save", type=str, default="test", help="file name to save")
parser.add_argument("--load", type=str, default=".", help="file name to load")
parser.add_argument("--print_model", action="store_true", help="print model")
parser.add_argument(
    "--save_models", action="store_true", help="save all intermediate models"
)
parser.add_argument(
    "--model_best_loss",
    type=float,
    default=-1,
    help="save model if its loss < model_best_loss",
)
parser.add_argument(
    "--print_every",
    type=int,
    default=100,
    help="how many batches to wait before logging training status",
)
parser.add_argument("--save_results", action="store_true", help="save output results")

args = parser.parse_args()
template.set_template(args)

args.scale = list(map(lambda x: int(x), args.scale.split("+")))

if args.epochs == 0:
    args.epochs = 1e8

for arg in vars(args):
    print(arg)

    if vars(args)[arg] == "True":
        vars(args)[arg] = True
    elif vars(args)[arg] == "False":
        vars(args)[arg] = False
